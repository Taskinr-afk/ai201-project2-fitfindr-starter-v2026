#!/usr/bin/env python3
"""
Re-score C2 across a MIX of hit counts (5 many-hit + 5 zero-hit per trial),
from the existing log without re-running the API calls.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "logs" / "requests.jsonl"

# Pull /ask-shaped records only (ok or no_match), skip bad_request.
records = []
with LOG.open("r", encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        if r.get("status") in ("ok", "no_match"):
            records.append(r)

# Milestone 3 ran 10 /ask requests. Milestone 5 ran 3 batches of 20 each.
# So the last 60 /ask records are the three M5 batches, oldest first.
m5 = records[-60:]
batches = [m5[0:20], m5[20:40], m5[40:60]]

# From each batch of 20, pick 10 with a true mix:
# indices 0,2,4,6,8 (first half = many-hit queries) and 10..14 (zero-hit queries).
MIX_IDX = [0, 2, 4, 6, 8, 10, 11, 12, 13, 14]

print("| Trial | passes | detail |")
print("|---|---|---|")
for t, batch in enumerate(batches, 1):
    sample = [batch[i] for i in MIX_IDX]
    passes = 0
    rows = []
    for r in sample:
        hits = r.get("search_hits", 0)
        ran = r.get("comparison_ran", False)
        expected = hits >= 2
        ok = ran == expected
        passes += int(ok)
        rows.append((r.get("query", "")[:30], hits, ran, expected, ok))
    print(f"| trial {t} | {passes}/10 | mix of hit counts |")
    for q, h, ra, ex, ok in rows:
        mark = "OK" if ok else "FAIL"
        print(f"      [{mark}] {q:30s} hits={h:>2} ran={str(ra):5s} expected={ex}")
    print()
