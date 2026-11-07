# Chapter 3 — Spreadsheet-Level Dataset Prep

## Your dataset starts as three columns

Forget JSONL for a moment. Open any spreadsheet app (LibreOffice Calc, Excel, Numbers, Google Sheets if you must). Make three columns:

| `instruction` | `input` | `output` |
| --- | --- | --- |
| Turn this shift note into a tidy SBAR summary. | *messy note text…* | *the tidy SBAR version…* |
| Turn this shift note into a tidy SBAR summary. | *a different messy note…* | *another tidy SBAR…* |
| Classify this customer email by intent. | *email text…* | `billing` |

- **instruction** — the task, phrased the way you would say it at inference time. Usually identical in every row for a single-purpose model; that is fine and even good.
- **input** — the material to work from. Leave it empty for ask-and-answer style rows.
- **output** — *exactly* what you wish the model to produce. Not "approximately." This column is the entire lesson; the model learns your letter.

Spreadsheet rules that save heartbreak:

1. **One row, one example.** No multi-task monsters.
2. **Output column answers the instruction the way you'd want to receive it** — same structure, same tone, every row. Consistency here *is* the fine-tune.
3. **Real-ish examples only.** Write them or gather them from real interactions; do not generate them from a model and describe that round-trip honestly if you do (model-made data trained on model output can echo quirks back amplified).
4. **No invented facts** in outputs. If the input does not contain a fact, the output must not contain it. You are teaching truthfulness with every row.
5. **Private data stays home.** Names, IDs, patient details — use fictional or heavily disguised examples. Never put real personal data into a training file you might upload or share later.

## How many rows?

| Rows of clean data | What it can teach |
| --- | --- |
| 20–50 | Only a demo; expect memorization, not generalization |
| 100–300 | A narrow habit: one format, one tone, one task |
| 500–2,000 | Comfortable single-purpose models |
| 5,000+ | Multi-task or robustness work (you likely outgrew this manual) |

A trustworthy 150 beats a sloppy 1,000. Quality gap matters more than quantity gap at this scale.

## From spreadsheet to JSONL (ten lines of Python)

Every training tool consumes **JSONL**: one JSON object per line. The common chat format is:

```json
{"messages": [{"role": "system", "content": "You reply in tidy SBAR format."}, {"role": "user", "content": "INSTRUCTION + INPUT HERE"}, {"role": "assistant", "content": "OUTPUT HERE"}]}
```

A tiny script turns your CSV into JSONL — this repo ships one, `tools/csv_to_jsonl.py`:

```bash
python3 tools/csv_to_jsonl.py dataset.csv dataset.jsonl
```

It validates as it goes: 3 columns exactly, no empty outputs, flags rows so long they would blow your context budget. Non-negotiable outputs:

- **A training file** (~90% of rows).
- **A held-out test file** (~10%, *never trained on*). Write the split before you look at results; the split is your honesty anchor in [Chapter 5](05-checking-results-honestly.md).

## Cleaning passes (each is ten minutes, all matter)

1. **Read every output once.** Out loud if it matters — you will catch half your errors this way.
2. **Deduplicate.** Near-duplicate rows overweight whatever they say. A `sort` and a squint catches most.
3. **Length check.** Rows that overflow the model's context get silently truncated during training — a truncated example teaches truncation. Keep inputs comfortably short.
4. **Consistency check.** If 30% of rows end with a period and 70% do not, the model will learn a coin flip. Pick one behavior.
5. **Balance check.** One task should not be 90% of rows when you meant to teach two tasks; the small task will be learned at 10% strength.
6. **Contradiction check.** Two rows asking the same thing with different answers = the model learns to vary, not to obey. Resolve deliberately.

> **The one-origin rule:** every output row traces to a *reason* you could defend — "this is how a good answer looks." If you cannot say why an output is good, do not train on it. The model will not figure out your intention; it will average it.

## Common beginner mistakes (ranked by pain caused)

1. Trash-data training ("it's fine, more data is more better" — it is not).
2. No held-out test set, then "it works great" because they quote training-set prompts back at it.
3. Inventing the license/limit/price *inside* output rows and then being surprised the model invents things.
4. One enormous prompt in `instruction` containing the few-shot examples meant for *inference time* only.
5. CSV comma-breakage from embedding multi-line text without proper quoting — use the script; it handles escaping.

When the spreadsheet is clean, you are one honest afternoon away from [Chapter 4](04-training-on-an-ordinary-pc.md).
