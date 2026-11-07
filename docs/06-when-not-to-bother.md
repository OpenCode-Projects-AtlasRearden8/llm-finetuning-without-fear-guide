# Chapter 6 — When Not to Bother

## Chapter zero of every fine-tuning project

This is the shortest chapter in the manual and possibly the most valuable. Fine-tuning is a *weekend-shape* activity — a few evenings and a Sunday, honestly budgeted. It is not free. And there are failures to avoid that are quietly expensive:

- **Opportunity cost:** the Saturday you spent tuning a LoRA you did not need.
- **Maintenance cost:** a model you must now re-train whenever your style changes.
- **Trust cost:** shipping "fine-tuned!" branding on something a prompt would do better, and users noticing.

Here are the not-to-bother cases, in full.

## 1. "I want it to know my documents"

That is retrieval (RAG), not fine-tuning. The model reads a fetched chunk at answer time. Fine-tuning a model on your docs gives you an unreliable mixture of paraphrase and memorization that will confidently misquote you. Companion manual: *rag-your-docs-handbook*.

## 2. "I want it to follow a rule or two"

That is a system prompt. Cost: one sentence. Fine-tuning adds nothing but risk.

## 3. "I want frontier-level intelligence on my hobby GPU"

LoRA adds habit, not IQ. A 3B model with a beautiful sleeve still reasons like a 3B model. If the task needs deeper reasoning, use a bigger model via prompt+retrieval, or simplify the task into small steps the small model can do.

## 4. "I have 25 examples"

Below ~100 rows, a LoRA mostly memorizes. Put those 25 hours into writing a superb prompt with few-shot examples instead — same effort, better ROI at that scale.

## 5. "Something is wrong with every output and I don't know what"

Undefined requirements cannot be fine-tuned into existence. Write the success criteria down first (three bullets is fine). If you cannot state what "good" looks like, no model — or dataset — can learn it. Fix the spec, then decide again.

## 6. "I want the facts in my outputs to always be current/correct"

Fine-tuning is a snapshot of habits, not a live database. Prices, policies, inventories: retrieval. (Healthcare anyone reading this: this also applies to anything clinical. Education only; never medical decisions.)

## 7. "It sounds impressive"

If the *real* motivation is the badge, skip it. Get the result with a prompt first, then claim "fine-tuned" in your README only when the measured table from [Chapter 5](05-checking-results-honestly.md) backs it up. The badge is a loan against those numbers, not against the word itself.

## The quick triage

| If your real goal is… | Do this instead |
| --- | --- |
| Answer from my documents | RAG / retrieval + prompt |
| Follow 1–5 formatting rules | System prompt |
| Better reasoning | Bigger model, or decompose the task |
| 25 examples of a pattern | Few-shot prompt |
| Current facts out | Retrieval or a pipeline, not weights |
| A reliable *habit/shape* on a small model | Yes — LoRA. Welcome back to Chapters 3–5 |

## The one good reason that isn't on this list but should be discussed

**Learning.** If your honest goal is "I want to understand how this works, build one, and be able to say I did" — that is a *great* reason, and this manual's Chapters 3–5 are the safe path: small model, clean 150-row dataset, honest held-out test. Knowledge gained is never an opportunity cost. Just don't ship it as if it were a product; ship it as a learning artifact with its three summary numbers from Chapter 5.

Now the wrap-up: [Chapter 7 — Quick Reference and Glossary](07-quick-reference-and-glossary.md).
