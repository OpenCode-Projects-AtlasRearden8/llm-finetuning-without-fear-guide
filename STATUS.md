# STATUS.md — Fine-Tuning Without Fear

Built 2026-11-07 · single commit `6375d0b` · all 18 verification checks pass.

## What was built

A beginner's manual on LLM fine-tuning ("Fine-Tuning Without Fear") with a static HTML site, all local-first:

- **`docs/` — the manual (8 markdown files, source of truth).** Start-here index plus 7 chapters: (1) what fine-tuning actually is (habits-not-facts framing, LoRA explained with no math), (2) when LoRA beats prompting (decision chart, worked example, yes-count scorecard), (3) spreadsheet-level dataset prep (3-column CSV → JSONL, row-count expectations, six cleaning passes, common mistakes), (4) training on an ordinary PC (model-size/RAM table, MLX vs Unsloth vs LLaMA-Factory vs free Colab, universal recipe, loss-curve reading), (5) checking results honestly (held-out rule, blind A/B vs base model, forgetting check, warning signs, 3-number summary), (6) when not to bother (7 skip-it cases + triage table), (7) one-page recipe + plain-English glossary.
- **`site/` — static HTML site** built from the docs: 8 pages + stylesheet. System fonts, no JavaScript, no CDN assets, no analytics, no accounts. Committed pre-built so it opens directly.
- **`build.py`** — stdlib-only markdown→HTML site builder (headings, tables, fenced code, blockquotes, nested lists, inline code/bold/italic/links, cross-page `.md`→`.html` link rewriting with heading anchors).
- **`tools/csv_to_jsonl.py`** — dataset converter: 3-column CSV → chat-JSONL with train/test split (`--test`, `--test-frac`, `--system`). Validates columns, drops broken/empty/duplicate rows, reports problems on stderr, exits non-zero if anything was dropped.
- **`verify.py`** — 18 checks: site build, per-page HTML well-formedness (tag balance, charset/viewport/css/lang), heading-anchor collection, all internal link resolution, stylesheet presence, converter self-test (broken-CSV exit code + split sizes + JSONL shape), LICENSE copyright exactness, README credit, and a repo-wide secrets scan.
- **`README.md`, `LICENSE` (MIT, "Copyright (c) 2026 Asdale Dynamics, LLC"), `.gitignore`.** Git initialized; one commit as the existing identity; no pushes, no remotes.

## How to run it

```bash
python3 build.py      # rebuild site/ from docs/ (stdlib only, offline)
python3 verify.py     # build + HTML + links + converter self-test
open site/index.html  # read the site (pre-built, so usually not needed)
python3 tools/csv_to_jsonl.py my.csv train.jsonl --test test.jsonl --test-frac 0.1
```

Requires Python 3.10+. No pip installs, no network, no API keys, no cloud accounts.

## Verification results

`python3 verify.py` → **all 18 checks passed** (site builds; 8 pages well-formed; links/anchors resolve; converter self-test passes on clean and broken CSVs; LICENSE line exact; no secrets found). Manual training itself was not executed here — see gaps below.

## Known gaps

- **No model actually trained in this repo.** Chapters 4–5 describe MLX/Unsloth/LLaMA-Factory accurately in general terms (r=16/alpha=32, LR 2e-4, 2 epochs) but no end-to-end training run was performed to prove those exact flags against current tool versions — re-check each tool's docs as they move fast.
- **No sample dataset shipped.** The converter is tested in-verify, but the repo has no example CSV to click-through (a small fictional-example dataset would be a nice follow-up).
- **Converter covers the markdown subset this manual uses** (no images, footnotes, or task lists). Unusual markdown may render as-is text.
- **No CI and no GitHub Pages wiring** (by design — no publishing was requested).
- Chapter 2's healthcare example is education-only formatting practice; it deliberately avoids clinical advice, but that boundary should not be blurred if the content is ever republished beyond education.
