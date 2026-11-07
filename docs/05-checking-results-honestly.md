# Chapter 5 — Checking Results Honestly

## The hands-off rule

Everything in this chapter flows from one rule:

> **Never judge a fine-tune on data it trained on.** If you ask it a question whose answer it memorized, you are grading the photocopier.

Your held-out test file ([Chapter 3](03-dataset-prep-spreadsheet-level.md)) exists only for this chapter. If you peeked at test results and then adjusted the model repeatedly, make a *fresh* holdout from new rows — otherwise tests get stale ("test set leakage by repetition").

## The comparison that means something

Run the *same* held-out prompts through:

- **A:** the base model, no adapter
- **B:** base model + your LoRA
- **C (optional):** base model + your best hand-written prompt

Score blind if you can: mix A and B answers, shuffle, read without labels. This kills the biggest measurement error of all — *wanting it to have worked*. You invested evenings; you will see improvement unless you blind yourself on purpose.

## What to actually measure

For a **format habit** (the most common beginner fine-tune):

- **Format pass rate:** % of held-out outputs that have the right structure — count them, don't eyeball-gesture. A simple checklist scored 1/0 per row: right sections? right order? no additions?
- **Instruction following:** did it do *only* what was asked?
- **Stability:** run each test prompt 2–3 times (chat models are temperature-noisy); "usually right" is a real result, "right once" is not.

For **style/voice**: side-by-side pairs, blind, your pick rate vs coin-flip 50%.

Keep a tiny results table — 15 minutes, and weeks later it is the only thing you will trust:

| Test set | Format pass | Stability | Notes |
| --- | --- | --- | --- |
| Base model | 12% | — | reads prompt, ignores half |
| LoRA v1 | 84% | 2/3 runs | ranting in section 3 |
| LoRA v2 (1 epoch) | 91% | 3/3 | keep this one |

## The forgetting check (the one everyone skips)

Fine-tunes can *steal* ability from elsewhere. Ask your fine-tuned model a handful of **off-task questions** — general chit-chat, simple arithmetic, summarizing a paragraph — where the *base* model was fine. If the LoRA made it suddenly unable to do those things, you trained too hard: fewer epochs, lower learning rate, or raise `r` a bit. A good single-purpose sleeve mostly leaves the rest alone.

## Warning signs you memorized instead of learned

- Held-out answers **copied a training row verbatim**, including details the input never mentioned.
- **Perfect** scores on near-duplicates but nonsense on slight rewordings of the same ask ("turn this into SBAR" works; "give me the SBAR summary" flops).
- Loss on training data near zero while test format pass rates sit low.

Fix, in order of gentleness: fewer epochs → smaller `r` → learning rate down → more (and more varied) data.

## Honest failure statement template

Because this manual stands for honesty, here is language for your own README after v1:

> *Measured on 20 held-out examples: format compliance 91% (base model, 12%). Known regressions: long inputs over ~2,000 characters degrade. Not intended for general chat.*

One paragraph like that earns you everything a hype-post claiming perfection costs you in credibility.

## The three-number summary

When you finish testing, write down exactly three things: **pass rate on held-out data**, **pass rate of base model on the same data**, and **one honest limitation**. If all three exist, your project is a success regardless of pretty the numbers are — you measured like a scientist instead of hoping like a fan.

Next: [Chapter 6 — When Not to Bother](06-when-not-to-bother.md).
