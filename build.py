#!/usr/bin/env python3
"""Build the static HTML site from the markdown manual in docs/.

Stdlib only. Converts the markdown subset used by this manual
(headings, paragraphs, pipe tables, fenced code, blockquotes,
bulleted/numbered lists, horizontal rules, and inline code, bold,
italic, bold-italic, and links) into clean HTML pages in site/.

Usage: python3 build.py
"""

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"[^a-z0-9 ]", "", text).strip()
    return re.sub(r"\s+", "-", text)


def convert_inline(md: str) -> str:
    """Inline markdown (code, links, bold, italic) to HTML."""
    placeholders = []

    def stash(html_text: str) -> str:
        placeholders.append(html_text)
        return f"\x00{len(placeholders) - 1}\x00"

    text = html.escape(md, quote=False)
    # inline code (protect it from further processing)
    text = re.sub(r"`([^`]+)`", lambda m: stash(f"<code>{m.group(1)}</code>"), text)
    # links: bare http(s) URLs and [label](target)
    text = re.sub(r"(?<![\"'>=\w])(https?://[^\s\)<]+)",
                  lambda m: stash(f'<a href="{m.group(1)}">{m.group(1)}</a>'), text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: _link(m.group(1), m.group(2), stash), text)
    # bold-italic, bold, italic (bold may wrap italic)
    text = re.sub(r"\*\*\*(.+?)\*\*\*",
                  lambda m: f"<strong><em>{m.group(1)}</em></strong>", text)
    text = re.sub(
        r"\*\*(.+?)\*\*",
        lambda m: "<strong>" + re.sub(r"\*(.+?)\*", r"<em>\1</em>", m.group(1)) + "</strong>",
        text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)
    for i, replacement in enumerate(placeholders):
        text = text.replace(f"\x00{i}\x00", replacement)
    return text


def _link(label: str, target: str, stash) -> str:
    if re.match(r"https?://", target):
        href = html.escape(target, quote=True)
    else:
        href = html.escape(re.sub(r"\.md(#.*)?$", r".html\1", target), quote=True)
    return stash(f'<a href="{href}">{label}</a>')


def render_markdown(md_text: str) -> str:
    lines = md_text.splitlines()
    out = []
    i = 0
    list_stack = []  # current open list tags: 'ul' / 'ol'

    def close_lists():
        while list_stack:
            out.append(f"</{list_stack.pop()}>")

    while i < len(lines):
        line = lines[i]

        # fenced code block
        if line.startswith("```"):
            close_lists()
            lang = line[3:].strip()
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            cls = f' class="lang-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(code))}</code></pre>")
            continue

        # blockquote (possibly multi-line, may contain a list)
        if line.startswith(">"):
            close_lists()
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            rendered, _ = _render_block("\n".join(quote))
            out.append(f"<blockquote>{rendered}</blockquote>")
            continue

        # table: header row then separator row
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            close_lists()
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            body = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                body.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append("<table><thead>")
            out.append("<tr>" + "".join(f"<th>{convert_inline(c)}</th>" for c in header) + "</tr>")
            out.append("</thead><tbody>")
            for row in body:
                row += [""] * (len(header) - len(row))
                out.append("<tr>" + "".join(f"<td>{convert_inline(c)}</td>" for c in row[:len(header)]) + "</tr>")
            out.append("</tbody></table>")
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_lists()
            level = len(m.group(1))
            inline = convert_inline(m.group(2).strip())
            out.append(f'<h{level} id="{slugify(m.group(2))}">{inline}</h{level}>')
            i += 1
            continue

        if re.match(r"^\s*(---+|\*\*\*+)\s*$", line):
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        # lists (two levels: 2-space indent nesting)
        m = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", line)
        if m:
            indent, marker, content = m.groups()
            depth = 1 if len(indent) >= 2 else 0
            ordered = bool(re.match(r"\d", marker))
            tag = "ol" if ordered else "ul"
            while len(list_stack) > depth + 1:
                out.append(f"</{list_stack.pop()}>")
            while len(list_stack) < depth + 1:
                list_stack.append(tag)
                out.append(f"<{tag}>")
            inner = convert_inline(content.strip())
            out.append(f"<li>{inner}</li>")
            i += 1
            continue

        if not line.strip():
            close_lists()
            i += 1
            continue

        # paragraph (consecutive non-empty lines, stop at blank line or next block)
        para = [line]
        while True:
            i += 1
            if i >= len(lines) or not lines[i].strip() or re.match(r"^(#{1,6}\s|```|>|\s*[-*]\s|\s*\d+[.)]\s|\s*---+\s*$)", lines[i]) or "|" in lines[i]:
                break
            para.append(lines[i])
        text = convert_inline(" ".join(p.strip() for p in para))
        out.append(f"<p>{text}</p>")
    close_lists()
    # strip any empty nested lists that may have been left open
    return "\n".join(out)


def _render_block(md_text: str):
    """Render a nested partial document (used by blockquotes)."""
    inner = render_markdown(md_text)
    return inner, None


def build_page(body: str, title: str, chapter_no: int | None) -> str:
    nav = []
    for j, (href, label) in enumerate(chapters):
        current = ' class="current"' if j == chapter_no else ""
        nav.append(f"<li><a{current} href=\"{href}\">{label}</a></li>")
    return PAGE_TEMPLATE.format(
        title=title, nav="".join(nav), body=body,
    )


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Fine-Tuning Without Fear - a beginner's manual by Asdale Dynamics, LLC">
<title>{title} · Fine-Tuning Without Fear</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<nav>
<ul>
{nav}
</ul>
</nav>
<main>
{body}
</main>
<footer>
<p>Fine-Tuning Without Fear &middot; Copyright (c) 2026 Asdale Dynamics, LLC &middot; <a href="https://dylanasdale.github.io">dylanasdale.github.io</a></p>
<p>No tracking. No accounts. No fonts fetched from the internet.</p>
</footer>
</body>
</html>
"""

chapters: list[tuple[str, str]] = []


def first_heading(md_text: str) -> str:
    for line in md_text.splitlines():
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            return m.group(1).strip()
    return "Untitled"


def main() -> None:
    md_files = sorted(DOCS.glob("*.md"))
    # keep the manual's reading order instead of alphabetical
    order = ["index.md"] + [p.name for p in sorted(DOCS.glob("0*.md"))]
    md_files = [DOCS / n for n in dict.fromkeys(order) if (DOCS / n).exists()]

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    shutil.copyfile(ROOT / "site-src" / "style.css", SITE / "style.css")

    pages = []
    for md_file in md_files:
        md_text = md_file.read_text(encoding="utf-8")
        body = render_markdown(md_text)
        title = first_heading(md_text)
        href = md_file.stem + ".html"
        pages.append((href, title, body, md_text))

    chapters.clear()
    for idx, (href, title, _body, _md) in enumerate(pages):
        short = "Start here" if href == "index.html" else title
        chapters.append((href, short))

    for idx, (href, title, body, _md) in enumerate(pages):
        page = build_page(body, title, idx)
        (SITE / href).write_text(page, encoding="utf-8")
        print(f"built site/{href}")

    print(f"site build complete: {len(pages)} pages")


if __name__ == "__main__":
    main()
