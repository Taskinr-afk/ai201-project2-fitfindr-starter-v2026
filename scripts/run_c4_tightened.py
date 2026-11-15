#!/usr/bin/env python3
"""
Milestone 6 — tightened C4. Runs 10 bad-request payload variants three times
against a running serve.py and reports HTTP status + logged status per payload.

Usage:
    python scripts/run_c4_tightened.py --label before
    python scripts/run_c4_tightened.py --label after

Writes results/capstone_c4_<label>.md.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

os.environ["AI201_CACHE"] = "0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "logs" / "requests.jsonl"

PAYLOADS = [
    # original 5 (missing / empty)
    ("empty object",                b"{}",                                   "application/json"),
    ("empty string query",          b'{"query": ""}',                        "application/json"),
    ("whitespace query",            b'{"query": "   "}',                     "application/json"),
    ("wardrobe only, no query",     b'{"wardrobe": {"items": []}}',          "application/json"),
    ("null query",                  b'{"query": null}',                      "application/json"),
    # 5 tightened: ill-typed query
    ("query as list",               b'{"query": [1,2,3]}',                   "application/json"),
    ("query as number",             b'{"query": 42}',                        "application/json"),
    ("query as bool",               b'{"query": true}',                      "application/json"),
    ("query as object",             b'{"query": {"nested": "x"}}',           "application/json"),
    ("no content-type header",      b'{"query": "vintage tee"}',             None),
]


def line_count(path):
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def read_new_records(path, start):
    if not path.exists():
        return []
    out = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < start:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def run_trial():
    """Fire all 10 payloads one at a time. For each, read the one new log line
    (if any) immediately so matching isn't thrown off by payloads that log
    nothing."""
    results = []
    for name, body, ctype in PAYLOADS:
        before = line_count(LOG_FILE)
        headers = {}
        if ctype:
            headers["Content-Type"] = ctype
        req = urllib.request.Request("http://localhost:5000/ask", data=body, headers=headers)
        http = None
        try:
            urllib.request.urlopen(req, timeout=30).read()
            http = 200
        except urllib.error.HTTPError as e:
            http = e.code
        except Exception as e:
            http = f"err:{e}"
        time.sleep(0.05)  # let the log write flush
        new = read_new_records(LOG_FILE, before)
        logged_status = new[0].get("status") if new else "<NO LOG>"
        results.append({
            "name": name, "http": http, "logged_status": logged_status,
            "pass": http == 400 and logged_status == "bad_request",
        })
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True, choices=["before", "after"])
    args = ap.parse_args()

    srv = subprocess.Popen(
        [sys.executable, "serve.py"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        env={**os.environ}, cwd=str(ROOT),
    )
    time.sleep(3)

    trials = []
    try:
        for t in range(1, 4):
            print(f"\n--- trial {t} ---")
            results = run_trial()
            passes = sum(int(r["pass"]) for r in results)
            trials.append((passes, results))
            for r in results:
                mark = "OK" if r["pass"] else "FAIL"
                print(f"  [{mark}] {r['name']:30s} http={r['http']}  logged={r['logged_status']}")
            print(f"  trial {t}: {passes}/10")
    finally:
        srv.terminate()
        srv.wait(timeout=5)

    out_path = ROOT / "results" / f"capstone_c4_{args.label}.md"
    lines = [f"# C4 tightened — {args.label.upper()}\n"]
    lines.append("| Trial | Passes | Details |")
    lines.append("|---|---|---|")
    for t, (passes, _) in enumerate(trials, 1):
        lines.append(f"| trial {t} | {passes}/10 | 10 payload variants: 5 original + 5 ill-typed |")
    lines.append("\n## Per-payload results (trial 3)\n```")
    for r in trials[-1][1]:
        mark = "OK" if r["pass"] else "FAIL"
        lines.append(f"  [{mark}] {r['name']:30s} http={str(r['http']):>5s}  logged_status={r['logged_status']}")
    lines.append("```\n")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
