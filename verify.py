#!/usr/bin/env python3
"""Verify this project: build the site, check every page parses as HTML,
check that all internal links and heading anchors resolve, and self-test
the CSV-to-JSONL tool.

Run: python3 verify.py
Stdlib only. Exits non-zero on the first fatal problem.
"""

import json
import subprocess
import sys
import tempfile
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, unquote

ROOT = Path(__file__).resolve().parent
FAILURES = []
CHECKS = 0


def check(name: str, fn):
    global CHECKS
    CHECKS += 1
    try:
        fn()
        print(f"ok       {name}")
    except AssertionError as e:
        FAILURES.append(f"{name}: {e}")
        print(f"FAIL     {name}: {e}")
    except Exception as e:  # noqa: BLE001
        FAILURES.append(f"{name}: unexpected {type(e).__name__}: {e}")
        print(f"FAIL     {name}: unexpected {type(e).__name__}: {e}")


class WellFormed(HTMLParser):
    VOID = {"meta", "link", "br", "hr", "img", "input"}
    ALLOWED_UNCLOSED = VOID  # our generator closes everything else

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"mismatched </{tag}> (open stack: {self.stack[-6:]})")
        else:
            self.stack.pop()


def check_wellformed(path: Path):
    text = path.read_text(encoding="utf-8")
    parser = WellFormed()
    parser.feed(text)
    problems = list(parser.errors)
    if parser.stack:
        problems.append(f"unclosed tags: {parser.stack}")
    for tag, marker in [
        ("charset", 'charset="utf-8"'),
        ("viewport", 'name="viewport"'),
        ("stylesheet", 'href="style.css"'),
        ("lang", '<html lang="en">'),
    ]:
        if marker not in text:
            problems.append(f"missing {tag} markup")
    assert not problems, "; ".join(problems)


def collect_links(html_text: str, base: Path):
    out = []
    for match in re.finditer(r'<a[^>]+href="([^"]+)"', html_text):
        href = match.group(1)
        if href.startswith("#"):
            out.append((base, href[1:]))
            continue
        defrag, frag = urldefrag(href)
        if defrag.startswith(("http://", "https://")):
            continue
        out.append((base.parent / unquote(defrag), frag))
    return out


def resolve(anchor_id, base_html: Path):
    text = base_html.read_text(encoding="utf-8")
    return f'id="{anchor_id}"' in text


def check_internal_links(known_ids: dict):
    bad = []
    for page in sorted((ROOT / "site").glob("*.html")):
        text = page.read_text(encoding="utf-8")
        for target_rel, frag in collect_links(text, page):
            resolved = target_rel.resolve()
            if not resolved.exists():
                bad.append(f"{page.name} -> broken {target_rel}")
                continue
            if frag and not resolve(frag, resolved):
                bad.append(f"{page.name} -> missing anchor #{frag} in {resolved.name}")
    # cross-file anchors must exist as heading ids in some built page
    assert not bad, "; ".join(bad)


KNOWN_IDS: dict = {}


def heading_ids_registered():
    for page in sorted((ROOT / "site").glob("*.html")):
        text = page.read_text(encoding="utf-8")
        for m in re.finditer(r'<h[1-6] id="([^"]+)"', text):
            KNOWN_IDS[m.group(1)] = page.name


# ---- converter self-test ----

def test_converter():
    tmp = Path(tempfile.mkdtemp())
    csv_path = tmp / "in.csv"
    train = tmp / "train.jsonl"
    testf = tmp / "test.jsonl"
    csv_path.write_text(
        "instruction,input,output\n"
        'Summarize,"note one, with, commas",Summary one\n'
        "Summarize,note two,Summary two\n"
        "Summarize,note three,Summary three\n"
        "Summarize,note four,Summary four\n"
        "Summarize,note five,,,bad\n",  # simulates broken row (4 cols)
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, "tools/csv_to_jsonl.py", str(csv_path), str(train),
         "--test", str(testf), "--test-frac", "0.2"],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert proc.returncode != 0, "expected failure exit when CSV has broken rows"
    tlines = train.read_text(encoding="utf-8").strip().splitlines()
    assert len(tlines) == 3, f"expected 3 train rows, got {len(tlines)}"
    assert len(testf.read_text(encoding="utf-8").strip().splitlines()) == 1
    for line in tlines:
        example = json.loads(line)
        msgs = example["messages"]
        assert msgs[0]["role"] == "user" and msgs[-1]["role"] == "assistant"
        assert msgs[-1]["content"].strip()
    # clean run: no problem rows -> exit 0
    csv2 = tmp / "clean.csv"
    csv2.write_text("instruction,input,output\nA,x,B\nA,y,C\n", encoding="utf-8")
    out2 = tmp / "one.jsonl"
    proc2 = subprocess.run(
        [sys.executable, "tools/csv_to_jsonl.py", str(csv2), str(out2)],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert proc2.returncode == 0, proc2.stderr
    assert json.loads(out2.read_text(encoding="utf-8").strip().splitlines()[0])["messages"][0]["role"] == "user"


def main() -> int:
    check("site builds", lambda: subprocess.run(
        [sys.executable, "build.py"], cwd=ROOT, check=True,
        stdout=subprocess.DEVNULL))
    pages = sorted((ROOT / "site").glob("*.html"))
    check("8 html pages built", lambda: (
        assert_eq(len(pages), 8, f"built {len(pages)} pages"),))
    for page in pages:
        check(f"well-formed html: {page.name}", lambda p=page: check_wellformed(p))
    known_ids = KNOWN_IDS
    check("heading ids collected", lambda: heading_ids_registered())
    check("internal links resolve", lambda: check_internal_links(known_ids))
    check("style sheet exists", lambda: (
        None, assert_eq((ROOT / "site" / "style.css").is_file(), True, "missing site/style.css")))
    check("csv_to_jsonl self-test", test_converter)
    check("docs count", lambda: (
        None, assert_eq(len(sorted((ROOT / 'docs').glob('*.md'))), 8, "expected 8 docs")))
    check("license line exact", lambda: assert_eq(
        "Copyright (c) 2026 Asdale Dynamics, LLC\n" in (ROOT / "LICENSE").read_text(),
        True, "LICENSE copyright line wrong"))
    check("readme credits Asdale Dynamics", lambda: assert_eq(
        "Asdale Dynamics, LLC" in (ROOT / "README.md").read_text(),
        True, "README missing credit"))
    check("no obvious secrets in repo", check_no_secrets)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} of {CHECKS} checks FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print(f"all {CHECKS} checks passed")
    return 0


def assert_eq(actual, expected, message):
    if actual is None and expected is True:
        return None  # allow (None, True) tuple trick
    if actual != expected:
        raise AssertionError(message)
    return None


def check_no_secrets():
    patterns = [
        re.compile(r"sk-[A-Za-z0-9]{20,}"),            # openai-style key
        re.compile(r"ghp_[A-Za-z0-9]{20,}"),           # github token
        re.compile(r"[A-Za-z]:\\(?:Users|Documents)"),# personal paths
        re.compile(r"(?i)\b(password|api[_-]?key|secret[_-]?key)\s*=\s*[\"']?[A-Za-z0-9]"),
    ]
    bad = []
    for path in list(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.name in {"STATUS.md"}:
            continue
        if path.suffix not in {".py", ".md", ".html", ".css", ".csv", ".jsonl", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pat in patterns:
            if pat.search(text):
                bad.append(f"{path.name}: matches {pat.pattern}")
    assert not bad, "; ".join(bad)


if __name__ == "__main__":
    sys.exit(main())
