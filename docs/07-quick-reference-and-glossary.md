# Chapter 7 — Quick Reference and Glossary

## The one-page recipe

1. **Decide** ([Ch. 2](02-when-lora-beats-prompting.md)): habit, not facts. Prompt-first prototype.
2. **Dataset** ([Ch. 3](03-dataset-prep-spreadsheet-level.md)): 3-column CSV → `tools/csv_to_jsonl.py` → train/test JSONL (90/10).
3. **Train** ([Ch. 4](04-training-on-an-ordinary-pc.md)): small model (1–4B, 4-bit), LoRA `r=16 alpha=32`, LR `2e-4`, 2 epochs, watch loss.
4. **Verify** ([Ch. 5](05-checking-results-honestly.md)): held-out prompts, blind A/B vs base model, format pass rate, forgetting check.
5. **Decide again** ([Ch. 6](06-when-not-to-bother.md)): ship only if the table says it beats the base model; otherwise keep the prompt.

Commands you will reuse:

```bash
python3 build.py                 # rebuild the HTML site
python3 verify.py                # run all checks (links, HTML, CSV→JSONL self-test)
python3 tools/csv_to_jsonl.py dataset.csv out.jsonl --test out-test.jsonl --test-frac 0.1
```

## Plain-English glossary

**Adapter** — the LoRA sleeve; a small file of habit-adjustments applied over a frozen base model.

**Base model** — the smart general model you start from, untouched under the sleeve.

**Checkpoint** — a saved snapshot; LoRA checkpoints are small, keep dated copies.

**Epoch** — one full pass over the training file. Two is a good default; more risks parroting.

**GGUF** — a compact single-file model format used by llama.cpp-class tools; often 4-bit quantized.

**LoRA / Low-Rank Adaptation** — training a tiny added layer instead of the whole model. Rank (`r`, capacity ceiling of the sleeve; 16 is a fine default) and alpha (a gain on the sleeve's influence, often 2× rank) are the two knobs from [Chapter 4](04-training-on-an-ordinary-pc.md).

**Merge** — bake the sleeve into the base weights so you ship a single standalone model. Optional; do it after testing.

**Overfit** — the model memorizes your rows instead of learning the underlying habit. Diagnosed in [Chapter 5](05-checking-results-honestly.md).

**PEFT** — parameter-efficient fine-tuning; the family of techniques (LoRA is its star) that makes small upgrades, on ordinary hardware.

**Prompt / system prompt** — instructions given to the model at run time; costs tokens on every call, unlike a fine-tune's baked habit.

**QLoRA** — LoRA applied over a 4-bit quantized base model; the reason a 3B LoRA fits in 8 GB (or less).

**Quantization** — storing the model's numbers more coarsely (4-bit ≈ 8× smaller than 16-bit). Loses a sliver of precision; keeps the brains.

**RAG (retrieval-augmented generation)** — fetching documents at answer time so the model reads facts instead of guessing them. The distinction from this manual is the subject of *rag-your-docs-handbook*.

**VRAM** — memory on a GPU. Rough guide for 4-bit QLoRA: model GB + 2–4 GB of overhead, on your GPU.

**Weights** — the model's learned numbers. "Full fine-tuning" moves them all; LoRA moves almost none of them.

## Where to go next

- *rag-your-docs-handbook* — retrieval when your problem is facts, not habits.
- *model-settings-decoded-guide* — temperature, top-p, and tokens: generation settings, decoded in the same plain voice.
- *The Massive AI Manual* (Dylan Asdale) — the friend explanations that started all this, at dylanasdale.github.io.

---

*Fine-Tuning Without Fear — educational content only. Copyright (c) 2026 Asdale Dynamics, LLC.*
