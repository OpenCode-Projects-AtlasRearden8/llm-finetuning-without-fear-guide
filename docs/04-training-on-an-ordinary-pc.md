# Chapter 4 — Training on an Ordinary PC

## Shop for the model first: sizes that fit real life

Small quantized model files (4-bit):

| Model size | .GGUF/.MLX 4-bit file | Rough fit |
| --- | --- | --- |
| ~0.5–1B | 0.4–0.8 GB | Old laptops |
| ~1–3B | 0.8–2 GB | Any modern 8 GB machine |
| ~3–7B | 2–5 GB | 16 GB machines, most 8 GB VRAM GPUs |
| 13B+ | 8 GB+ | Not this manual's territory |

Well-loved families in this range: **Qwen** (0.5B/1.5B/3B-class), **Llama 3.2** (1B/3B), **Phi-3-mini**, **Gemma 2/3** (2B/4B). All are strong trainers for single-purpose habits; quality differences at this size are smaller than dataset quality differences. That sentence deserves repeating: **your data quality beats their leaderboard position.**

## Pick your tool by your machine

| Your machine | Friendliest tool | Notes |
| --- | --- | --- |
| Apple Silicon Mac (M1–M4) | **MLX** (`mlx_lm.lora`) | Trains in unified memory; a 3B LoRA trains on a base 16 GB MacBook Air |
| Windows/Linux + NVIDIA GPU (6–12 GB VRAM) | **Unsloth** (Python notebooks/scripts) | 4-bit (QLoRA); a 3–4B model trains on 6–8 GB |
| Either, and you want a GUI | **LLaMA-Factory** | Web UI wrapping the same math; a touch heavier |
| No GPU, no Mac | **Free Colab (cloud)** | The only cloud mention in this manual; nothing to install, free tier trains 1–3B fine |

All three tools take the same JSONL you made in [Chapter 3](03-dataset-prep-spreadsheet-level.md) and produce a LoRA sleeve. That is not an accident: LoRA training is roughly *the same single GPU afternoon of math* everywhere; the tools are just different doors into the same room.

## The universal recipe (works with all three tools)

1. **Base model.** Download one small model in the chat instruct flavor, 4-bit where offered.
2. **Point at your JSONL** training and test files.
3. **Settings that are good starting points** for 1–4B models:
   - LoRA rank `r = 16`, `alpha = 32` (standard, sane)
   - learning rate ≈ `2e-4` (the classic LoRA default)
   - epochs = 2 (more risks parroting; check between epochs)
   - batch size as large as memory allows, gradient accumulation to taste
4. **Run, watch the loss.**
5. **Test on the held-out file.** Not vibes held-out — the file you split in Chapter 3.
6. **Save the adapter.** Usually some MBs. Copy it somewhere safe with a name that includes the date.

## What the loss curve is telling you

- **Falling fast near the start then flattening:** normal; it learned the broad shape.
- **Keeps falling low while your test file stops improving:** memorization beginning — stop earlier; fewer epochs.
- **Bounces wildly:** learning rate too high, or a few broken rows (see Chapter 3, cleaning passes).
- **Barely moves:** dataset too small, or the task teaches nothing a 2-epoch pass can express.

Do not aim for loss of exactly zero. Zero loss on training data usually means your model parrots your rows back and is useless on anything else — the classic overfitting tell, covered honestly in [Chapter 5](05-checking-results-honestly.md).

## Using what you trained

Options, cheapest first:

1. **llama.cpp / LM Studio / Ollama** — many accept a `.gguf` model *plus* a LoRA file, or a merged GGUF. Great for "try it tonight" testing.
2. **MLX (`mlx_lm.generate --model base --adapter my-lora`)** for Mac-native runs.
3. **Merge** (bake sleeve into weights) when you want one standalone file with no adapter plumbing — do it only after testing passes.

## The weekend plan that actually finishes

- **Hour 0–1:** pick model + tool, install.
- **Hour 1–3:** JSONL ready and validated (Chapter 3 script does the validation).
- **Then:** short smoke run — 30 rows, 1 epoch — *before* the long one. Ten minutes of smoke test saves some hours of full-data debugging.
- **Then:** the real run, 2 epochs, and the honest test in [Chapter 5](05-checking-results-honestly.md).
- Commiserate, retry on any failure with a smaller batch or 1 fewer epoch — most failures at this scale are memory or a data typo, not your intellect.

> **Set expectations for a first run:** your aim is not "publishable" but "provably better than the same small model without the sleeve, measured on the held-out file." Repeatable progress beats heroic one-shots.

Up next, the part most beginners skip (which is why their models disappoint): [Chapter 5 — Checking Results Honestly](05-checking-results-honestly.md).
