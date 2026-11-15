#!/usr/bin/env python3
"""
Measure the per-run cost of FitFindr — capstone Milestone 3.

Runs the agent N times with the cache DISABLED so every call actually hits the
model, captures tokens via generate.token_counts() and wall time via
time.perf_counter(), and prints the average.

Dollar figure uses the published Gemini 3.5 Flash-Lite rate at the top of this
file. The tokens are measured (not estimated) — the rate is the published one,
because that's the only thing you can multiply measured tokens by.

    python scripts/measure_cost.py              # 10 iterations, default queries
    python scripts/measure_cost.py --n 5        # fewer iterations
"""
import argparse
import os
import sys
import time
from pathlib import Path

# Force cache off before anything imports config or generate.
os.environ["AI201_CACHE"] = "0"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config  # noqa: E402,F401
import generate  # noqa: E402
from agent import run_agent  # noqa: E402
from utils.data_loader import get_example_wardrobe  # noqa: E402

# https://ai.google.dev/gemini-api/docs/pricing (Gemini 2.5/3.5 Flash-Lite tier)
# Quoted here so the arithmetic below is auditable.
PRICE_PER_1M_INPUT = 0.10
PRICE_PER_1M_OUTPUT = 0.40

QUERIES = [
    "vintage graphic tee under $30",
    "oversized flannel shirt size L",
    "y2k baby tee under $25",
    "corduroy jacket, M",
    "cargo pants size 30 under $40",
]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=10)
    args = p.parse_args()

    wardrobe = get_example_wardrobe()
    runs = []

    print(f"cache={os.environ.get('AI201_CACHE')} (0 = disabled)")
    print(f"running {args.n} queries...\n")

    for i in range(args.n):
        q = QUERIES[i % len(QUERIES)]
        before = generate.token_counts()
        t0 = time.perf_counter()
        session = run_agent(q, wardrobe)
        secs = time.perf_counter() - t0
        after = generate.token_counts()

        prompt = after["prompt"] - before["prompt"]
        out = after["output"] - before["output"]
        dollars = (prompt / 1_000_000) * PRICE_PER_1M_INPUT + (out / 1_000_000) * PRICE_PER_1M_OUTPUT
        status = "ok" if not session.get("error") else "no_match"
        runs.append({"q": q, "secs": secs, "prompt": prompt, "output": out, "usd": dollars, "status": status})
        print(f"  [{i+1:>2}] {secs:5.2f}s  prompt={prompt:>4}  output={out:>4}  ${dollars:.5f}  {status}  — {q}")

    def avg(key):
        return sum(r[key] for r in runs) / len(runs)

    print("\n──────── averages over", args.n, "runs ────────")
    print(f"  wall time:      {avg('secs'):.2f} s")
    print(f"  prompt tokens:  {avg('prompt'):.1f}")
    print(f"  output tokens:  {avg('output'):.1f}")
    print(f"  $ per run:      ${avg('usd'):.5f}")
    print(f"  $ per 100/day:  ${avg('usd') * 100:.4f}")


if __name__ == "__main__":
    main()
