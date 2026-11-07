# Fine-Tuning Without Fear

*A beginner's manual by Asdale Dynamics, LLC — plain English, step by step, never condescending.*

You have heard that you can "train your own AI model." You have maybe seen LoRA adapters, GPU jargon, and spreadsheet debates on the internet, and quietly wondered: *is this for me, or is this for people with data centers?*

This manual is the friend who sits down with you and says: here is what fine-tuning actually is, when it helps, when it is a waste of your weekend, and how to do a small, honest one on a normal computer. No cloud accounts required unless you want one. No secrets, no tracking, no hype.

## Read it in this order

1. [What fine-tuning actually is](01-what-fine-tuning-actually-is.md) — the plain-English explanation, with a perfume-counter analogy.
2. [When LoRA beats prompting](02-when-lora-beats-prompting.md) — the decision chart most people skip.
3. [Spreadsheet-level dataset prep](03-dataset-prep-spreadsheet-level.md) — yes, your dataset starts life as a CSV.
4. [Training on an ordinary PC](04-training-on-an-ordinary-pc.md) — real tools, real RAM numbers, small models.
5. [Checking results honestly](05-checking-results-honestly.md) — how to prove to yourself it worked (or didn't).
6. [When not to bother](06-when-not-to-bother.md) — the chapter some people buy this manual *for*.
7. [Quick reference and glossary](07-quick-reference-and-glossary.md) — cheat sheet and plain-English jargon decoder.

## The whole manual in four sentences

Fine-tuning adjusts how an existing model *behaves* — its format, tone, and habits — using examples you curate yourself, usually with a cheap technique called LoRA that trains a small "sleeve" instead of the whole model. It starts as a spreadsheet: prompt in one column, ideal answer in the next, maybe a hundred to a few thousand rows. Small models (1–4 billion parameters) run as 4-bit files that fit on an ordinary machine, and tools like MLX (Mac), Unsloth (Windows/Linux), or LLaMA-Factory (either) can train a LoRA on one over a lunch break. Fine-tuning teaches *habits*, not *facts* — if your goal is knowledge lookup, prompt tweaks or retrieval (RAG) usually win, and that discretion is the most valuable skill in this manual.

## How to use the HTML site

This repo ships a small static website built from these markdown files — no JavaScript frameworks, no fonts fetched from the internet, no cookies, no accounts. Open `site/index.html` in any browser after running `python3 build.py` (the built pages are also committed, so you may not even need to). See the README for details.

## Conventions used here

- Terms in [the glossary](07-quick-reference-and-glossary.md) are linked the first time they show up.
- Commands you can type look like `this`.
- Notes that could save your weekend are in blockquotes.
- *Honesty rule:* every "it worked" in this guide means "verified on examples the model never saw during training." If a chapter breaks that rule, it says so out loud.

---

*This manual is educational and general. It is not affiliated with any model vendor. Built with care by **Asdale Dynamics, LLC**.*
