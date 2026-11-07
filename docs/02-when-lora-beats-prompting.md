# Chapter 2 — When LoRA Beats Prompting

## The honest decision chart

Before you spend a Saturday on this, answer one question: **what would "success" look like, and could you get it by just writing a better prompt?**

### Use prompting or retrieval when...

- **The knowledge is the point.** Your product catalog, policy handbook, or troubleshooting logs. Retrieval (RAG) — the *rag-your-docs-handbook* territory — beats fine-tuning for factual lookup, because it hands the model a fresh document to read rather than hoping habits hold it.
- **The behavior change is a sentence long.** "Answer in two sentences, friendly, end with a question." Write it once, put it in the system prompt, done in a minute.
- **You will keep changing your mind.** A prompt is a Post-it note; a fine-tune is a haircut. Iteration is cheaper on paper first.
- **You want a model that still does *everything*.** Every fine-tune narrows specialization somewhat (see [Chapter 5](05-checking-results-honestly.md)); a prompt narrows nothing.

### Consider a LoRA when...

- **You have written the same 200-word style instructions so many times** that they are basically a policy document, and outputs still drift. Fine-tuning bakes the format in so you can stop paying the "prompt tax" every session.
- **Examples speak louder than instructions.** You have rows of *exactly* what good output looks like (support replies, structured forms, your book's voice). Models copy patterns better than they follow prose.
- **You need it to run on a small, free, or offline model.** A 1–3B model with a style LoRA can beat a general 7B model-with-long-prompt at a narrow job — and it runs on a laptop with no internet.
- **Latency or cost matters.** A short prompt always attached costs tokens on every request. A baked-in habit needs no prefix.
- **Your system prompt is long** because you keep rules and few-shot examples in it, repeated every session. Moving those habits into training data can shorten the prompt considerably.

### The hybrid truth

Most real projects end in layers:

1. **Prompt** for the experiment. Prove the job is possible *at all* with a large general model before fine-tuning anything.
2. **Retrieval** for the facts. Fine-tuning never replaces a notebook.
3. **Fine-tune** for the habit, once you have 100+ squeaky-clean examples and the prompt version is "works, but wobbly."

> **Rule of thumb: fine-tune the last thing, not the first thing.** If you cannot get the behavior right by prompting a big smart model with careful examples written by hand, fine-tuning your small model will not rescue it either. Sort that out first.

## A worked decision

Say your job: turn nurse-shift handover notes into a tidy SBAR-structured summary for a training simulation (education only, never medical decisions).

- Big model + a written SBAR prompt + three hand-tuned examples: *works, 4/5 close enough.* → prompt is nearly there; the remaining wobble is format drift.
- You want it to run on a small offline model for privacy. → the habit (SBAR structure) is exactly LoRA territory: many examples of "messy → tidy SBAR" teach structure better than a prompt does.
- The facts inside the note (names, meds, numbers): must come from the input note itself, never from training memory. → keep them in the input; the fine-tune only teaches the *shape*.

Conclusion: fine-tune the small model to *structure*, retrieve/keep-in-context the *facts*. That is the pattern to remember.

## Score card (count your honest "yes" answers)

| Statement | Yes? |
| --- | --- |
| I can describe the desired output shape precisely. | |
| I have (or can write) at least ~100 good example pairs. | |
| A plain prompt on a large model gets "close, but wobbly." | |
| I need a small/offline/cheap model to do this habit. | |
| The facts I need are in the inputs (or retrievable), not memorization. | |
| I am okay testing honestly before trusting it ([Ch. 5](05-checking-results-honestly.md)). | |

**0–2 yes:** write a better prompt, or read [Chapter 6](06-when-not-to-bother.md) and laugh with relief. **3–4:** prototype the prompt seriously; a LoRA may pay off. **5–6:** you are the target audience of [Chapter 3](03-dataset-prep-spreadsheet-level.md). Go get a spreadsheet open.

Next: [Chapter 3 — Spreadsheet-Level Dataset Prep](03-dataset-prep-spreadsheet-level.md).
