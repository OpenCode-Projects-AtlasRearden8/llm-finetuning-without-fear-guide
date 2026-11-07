# Chapter 1 — What Fine-Tuning Actually Is

## Start with the perfume counter

Picture a large language model as a hugely experienced person working behind a perfume counter. They have read almost everything ever written, they can talk about any subject, and they already know *hundreds* of ways to answer a question. If you ask something, you get a sensible, general answer.

Now imagine you hand that same person a one-page laminated card: *"When a customer asks a question, respond in exactly this style: warm, two sentences, always end with a suggested pairing."* They do not need to re-read their library. They just need to *tip their default behavior* toward your style.

That is fine-tuning in a nutshell:

> **Fine-tuning takes an already-smart model and nudges its *default habits* — format, tone, structure, and style — using a batch of curated examples.**

You are not teaching the model facts. It already read the internet. You are showing it *which version of itself* you want it to be.

## What changes (and what doesn't)

| Question | Fine-tuning | Prompting |
| --- | --- | --- |
| Can it change default tone/format? | Yes, permanently baked in | Yes, but restated every time |
| Can it add brand-new private facts? | Unreliably — habits aren't memory | Unreliably |
| Does the safety net stay? | Yes, a LoRA barely touches anything | Yes |
| Do you re-write instructions each session? | No, they're absorbed | Yes, every time |
| Does it work on top of any chat UI? | Yes, once merged or loaded as an adapter | Only where you can paste a prompt |

The fine-tuned model still has the same general knowledge, the same reasoning ability (more or less — see [Chapter 5](05-checking-results-honestly.md)), and the same base weights underneath, if you use LoRA. You made a well-read person adopt a style card.

## "Training a model" vs "fine-tuning": the same word, different prices

When someone says "we trained a model," they might mean:

1. **Pre-training** — building the model from scratch by reading trillions of words. Costs millions of dollars and months on thousands of GPUs. *Not this manual, and not your weekend.*
2. **Full fine-tuning** — updating *all* the billions of internal number-sliders ("weights") of an existing model. Requires serious GPU memory, and it is easy to do more harm than good (you can erase abilities the base model had).
3. **Parameter-efficient fine-tuning (PEFT)** — updating only a tiny added layer. **LoRA** is the friendly, affordable version of this, and it is what this manual uses from here on.

## LoRA, in one paragraph with no math

A LoRA ("Low-Rank Adaptation") saves a tiny *sleeve* — usually kilobytes to hundreds of megabytes — of adjustment values that sit alongside the frozen base model at inference time. Training it means only those sleeve numbers move; the original model is untouched. Because so few numbers move, it:

- Trains on hardware you actually own (even an 8 GB GPU, or a plain Mac).
- Trains fast — minutes to hours, not days.
- Keeps the base model safe; you can throw the sleeve away with no regret.
- Lets you keep several *styles* (a customer-service sleeve, a poetry sleeve, an FFXIV guild-news sleeve) around one shared base model.

Add the sleeve to the base model and the combination behaves like your fine-tuned version. Some people "bake it in" (merge) later, but that is optional.

## What fine-tuning is *bad* at (knowing this early saves you)

This deserves its plain English moment now, because half of all fine-tuning disappointment comes from forgetting it:

- **Facts.** A LoRA is a set of habits, not an encyclopedia in your pocket. Teaching it your 400 product SKUs and asking for exact recall is like teaching a student your inventory by habit without also giving them a notebook to check.
- **Reasoning power.** Fine-tuning will not make a 3B model out-think a frontier 100B+ model at tricky logic. It makes the small model reliable at the *shape* of work you trained on.
- **Cutting corners on data quality.** The model absorbs your examples *including their errors*. Typos in, typos out.

For facts, you want retrieval (what the companion *rag-your-docs-handbook* covers) or a careful pipeline. For habits, fine-tuning shines.

## The vocabulary you will see everywhere

- **Model / base model / weights:** the big file of learned numbers, e.g. a 4 GB file representing a 4B-parameter model.
- **Checkpoint:** a saved moment-in-time copy of the model.
- **Dataset:** the curated examples you train on. Yours starts life as a spreadsheet — [Chapter 3](03-dataset-prep-spreadsheet-level.md).
- **LoRA / adapter / sleeve:** the tiny trainable layer. See [the glossary](07-quick-reference-and-glossary.md) for the rest (Q, r, alpha, etc. when you are ready).
- **GPU / VRAM:** the graphics chip and its memory; a 4-bit small model plus training overhead fits in as little as 6–10 GB.
- **Epoch:** one full pass over your dataset. Two to three epochs is the common starting point.

Next: [Chapter 2 — When LoRA Beats Prompting](02-when-lora-beats-prompting.md), which asks the question *before* any setup: is this even the right tool?
