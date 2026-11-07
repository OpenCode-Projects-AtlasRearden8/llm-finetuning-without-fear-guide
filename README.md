# Fine-Tuning Without Fear

*A beginner's guide to fine-tuning your own small language model — plain English, step by step, never condescending.*

You can train a small AI model to write, format, and respond exactly the way you want — on an ordinary computer, with a spreadsheet, in a weekend. This manual shows you how, and (just as important) tells you when *not to bother*.

## What's inside

- [docs/index.md](docs/index.md) — start here; the reading order for all seven chapters
- **Chapter 1 · What fine-tuning actually is** — habits, not facts; what changes and what doesn't
- **Chapter 2 · When LoRA beats prompting** — the honest decision chart most people skip
- **Chapter 3 · Spreadsheet-level dataset prep** — your dataset starts life as a 3-column CSV
- **Chapter 4 · Training on an ordinary PC** — MLX, Unsloth, LLaMA-Factory; model sizes that fit real RAM
- **Chapter 5 · Checking results honestly** — held-out tests, blind comparison, the forgetting check
- **Chapter 6 · When not to bother** — seven ways to skip the whole project and still win
- **Chapter 7 · Quick reference and glossary** — the recipe on one page, jargon decoded

## Getting started

Everything is plain markdown in [`docs/`](docs/index.md). Read online-style via the built static site, or straight from the files.

### Build the HTML site

Requires Python 3.10+ (standard library only — no `pip install`, no network, no tracking):

```bash
python3 build.py     # builds site/ from docs/
```

Then open `site/index.html` in any browser. The built site is committed, too, so you can often just open it without building.

### Verify everything (build + link checks + tool self-test)

```bash
python3 verify.py
```

Runs the site build, confirms every page is well-formed HTML, checks that all internal links resolve, and self-tests the CSV→JSONL converter.

### Prep a dataset

Turn your 3-column spreadsheet (`instruction,input,output`) into training files with the held-out split the manual insists on:

```bash
python3 tools/csv_to_jsonl.py my-dataset.csv train.jsonl --test test.jsonl --test-frac 0.1
```

Training itself happens with standard open tools (MLX on a Mac, Unsloth or LLaMA-Factory on a PC) — see [Chapter 4](docs/04-training-on-an-ordinary-pc.md) for the settings that work on ordinary hardware.

## What this is not

- **Not a RAG guide.** Retrieval from your documents is a different manual — see the *rag-your-docs-handbook* companion.
- **Not a generation-settings guide.** Temperature, top-p, and output length live in *model-settings-decoded-guide*.
- **Not medical advice, ever.** One chapter uses nurse-shift handover notes purely as a worked formatting example; nothing here supports clinical decisions of any kind.
- **No cloud accounts, no API keys, no secrets.** The manual and tools run fully locally (the one cloud exception is a free hobbyist GPU notebook discussed generically).

## Repo layout

| Path | What it is |
| --- | --- |
| `docs/` | The manual (markdown, source of truth) |
| `site/` | Static HTML built from `docs/` (committed) |
| `site-src/` | Site stylesheet template used by the build |
| `tools/csv_to_jsonl.py` | CSV → JSONL dataset converter with train/test split |
| `build.py` | Docs → static site builder (stdlib only) |
| `verify.py` | Sanity checks: build, HTML well-formedness, links, tool self-test |

## Privacy first

- Static HTML only. No JavaScript frameworks, no analytics, no cookies, no font CDN — the site renders with system fonts.
- Building and verifying works entirely offline.
- Nothing in this repo contains secrets, API keys, or personal data. If you *contribute* a dataset example, disguise the real names and ID numbers first; [Chapter 3](docs/03-dataset-prep-spreadsheet-level.md) says why.

## More from the same voice

This guide is published by **Asdale Dynamics, LLC**, the independent studio behind *The Massive AI Manual* by Dylan Asdale — AI explained like a friend would, at [dylanasdale.github.io](https://dylanasdale.github.io). Companion manuals in the same family: *rag-your-docs-handbook* (retrieval) and *model-settings-decoded-guide* (generation parameters).

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

Educational content only; nothing here is professional advice of any kind.
