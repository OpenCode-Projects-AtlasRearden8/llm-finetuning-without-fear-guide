#!/usr/bin/env python3
"""Convert a 3-column CSV dataset (instruction,input,output) to JSONL
chat-format training files, with a held-out test split.

Checks as it goes: exactly 3 columns, non-empty instruction and output,
flagged duplicate and truncated rows — then writes the surviving rows to a
train file, holding out a fraction for testing. Dropped rows and duplicates
are reported on stderr; the exit code is non-zero if anything was dropped.

Usage:
  python3 tools/csv_to_jsonl.py dataset.csv train.jsonl [--test test.jsonl] [--test-frac 0.1] [--system "System prompt..."]

No network, no dependencies: standard library only.
"""

import argparse
import csv
import json
import random
import sys
from pathlib import Path

MAX_ROUNDS = 9  # warn loudly after this many flagged problems


def load_rows(csv_path: Path):
    rows, problems = [], []
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is not None:
            if [c.strip().lower() for c in header] == ["instruction", "input", "output"]:
                pass  # accepted, column order as documented
            elif len(header) == 3:
                print(f"note: header present but unexpected ({header}); using as data? No — skipping it.", file=sys.stderr)
        for lineno, raw in enumerate(reader, start=2):
            if not any(c.strip() for c in raw):
                continue
            if len(raw) != 3:
                problems.append(
                    f"line {lineno}: {len(raw)} of 3 columns; row dropped (re-export your CSV)"
                    if len(raw) > 3 else
                    f"line {lineno}: only {len(raw)} of 3 columns; row dropped")
                continue
            instruction, inp, output = (c.strip() for c in raw)
            if not instruction:
                problems.append(f"line {lineno}: empty instruction; row dropped")
                continue
            if not output:
                problems.append(f"line {lineno}: empty output (an output IS the lesson); row dropped")
                continue
            rows.append({"instruction": instruction, "input": inp, "output": output})
    # duplicate detection on (instruction, input)
    seen = {}
    usable = []
    for idx, r in enumerate(rows):
        key = (r["instruction"], r["input"])
        if key in seen:
            problems.append(f"row {idx + 1}: duplicate of row {seen[key] + 1}; duplicate dropped")
        else:
            seen[key] = idx
            usable.append(r)
    return usable, problems


def to_example(row, system_prompt):
    user_content = (row["instruction"] + "\n\n" + row["input"]).strip()
    example = {"messages": []}
    if system_prompt:
        example["messages"].append({"role": "system", "content": system_prompt})
    example["messages"].append({"role": "user", "content": user_content})
    example["messages"].append({"role": "assistant", "content": row["output"]})
    return example


def write_jsonl(rows, system_prompt, path: Path):
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(to_example(r, system_prompt), ensure_ascii=False) + "\n")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv_file", type=Path)
    p.add_argument("out_file", type=Path)
    p.add_argument("--test", type=Path, help="held-out test set output file (recommended)")
    p.add_argument("--test-frac", type=float, default=0.1, help="fraction held out for testing (default 0.1)")
    p.add_argument("--system", default="", help="optional system prompt added to every example")
    p.add_argument("--seed", type=int, default=2026, help="random seed for the split (default 2026)")
    args = p.parse_args()

    rows, problems = load_rows(args.csv_file)
    for prob in problems:
        print(f"problem: {prob}", file=sys.stderr)
    if problems:
        print(f"{len(problems)} problem(s) found — fix your CSV; flagged/broken rows were dropped.", file=sys.stderr)
    if not rows:
        print("no usable rows; nothing written.", file=sys.stderr)
        return 1
    if args.test is not None:
        if args.test_frac <= 0 or args.test_frac >= 1:
            raise SystemExit("--test-frac must be between 0 and 1 (exclusive)")
        if len(rows) < 20 and args.test_frac < 1.0:
            print(f"warning: only {len(rows)} rows — fine-tuning will mostly memorize at this size.", file=sys.stderr)
        n_test = max(1, round(len(rows) * args.test_frac))
        rng = random.Random(args.seed)
        indices = list(range(len(rows)))
        rng.shuffle(indices)
        test_idx = set(indices[:n_test])
        train_rows = [r for i, r in enumerate(rows) if i not in test_idx]
        test_rows = [r for i, r in enumerate(rows) if i in test_idx]
        write_jsonl(train_rows, args.system, args.out_file)
        write_jsonl(test_rows, args.system, args.test)
        print(f"wrote {len(train_rows)} train rows -> {args.out_file}")
        print(f"wrote {len(test_rows)} test rows -> {args.test}")
    else:
        write_jsonl(rows, args.system, args.out_file)
        print(f"wrote {len(rows)} rows -> {args.out_file}")
        print("note: no --test file produced. See docs/chapter 5: never judge a model on training data.")
    return 0 if not problems else 2


if __name__ == "__main__":
    sys.exit(main())
