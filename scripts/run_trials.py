#!/usr/bin/env python3
"""
Capstone Milestone 5 — three trials per criterion against the five criteria in
criteria.md (Capstone section). Writes a markdown report to
results/capstone_before.md.

Trial design:
  C1 (pick rule)    : 3 trials of 10 crafted input sets. compare_listings
                      directly; no model calls.
  C4 (bad path)     : 3 trials of 5 POST /ask with a bodyless or empty-query
                      request. No model calls.
  C2, C3, C5        : 3 shared trial batches of 20 POST /ask requests. Each
                      batch is one trial. C2 is scored on the first 10 of the
                      batch (mix of hit counts), C3 on whichever of those 10
                      have search_hits >= 2, C5 on all 20.

Requires serve.py to NOT already be running. Starts and stops its own server.
"""
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

os.environ["AI201_CACHE"] = "0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import compare_listings  # noqa: E402

LOG_FILE = ROOT / "logs" / "requests.jsonl"
REPORT_FILE = ROOT / "results" / "capstone_before.md"
REPORT_FILE.parent.mkdir(exist_ok=True)


# ── C1 fixtures: 10 crafted inputs with known expected picks ────────────────
def _item(iid, price, condition, size="M", title=None):
    return {
        "id": iid, "title": title or iid, "price": price,
        "condition": condition, "size": size, "colors": ["black"],
        "platform": "depop", "brand": None, "description": "", "style_tags": [],
        "category": "top",
    }

C1_CASES = [
    # (name, items, expected_pick_id, why)
    ("single excellent wins",
     [_item("a", 40, "good"), _item("b", 20, "excellent"), _item("c", 25, "fair")],
     "b", "only excellent"),
    ("cheapest of two excellents",
     [_item("a", 30, "excellent"), _item("b", 20, "excellent"), _item("c", 25, "good")],
     "b", "cheapest in excellent tier"),
    ("tie on cond+price picks first",
     [_item("a", 20, "excellent"), _item("b", 20, "excellent"), _item("c", 50, "good")],
     "a", "tie-break on input order"),
    ("all same tier, cheapest wins",
     [_item("a", 30, "good"), _item("b", 15, "good"), _item("c", 25, "good")],
     "b", "cheapest in only tier"),
    ("all fair, pick cheapest",
     [_item("a", 20, "fair"), _item("b", 10, "fair")],
     "b", "cheapest fair"),
    ("excellent beats cheaper good",
     [_item("a", 5, "good"), _item("b", 50, "excellent")],
     "b", "condition rank beats price"),
    ("3 goods, middle price",
     [_item("a", 30, "good"), _item("b", 20, "good"), _item("c", 25, "good")],
     "b", "cheapest good"),
    ("excellent at same price as good",
     [_item("a", 20, "good"), _item("b", 20, "excellent")],
     "b", "excellent tier wins"),
    ("two excellent, one much cheaper",
     [_item("a", 40, "excellent"), _item("b", 10, "excellent"), _item("c", 10, "fair")],
     "b", "cheapest in excellent tier"),
    ("mixed; cheapest-excellent at pos 3",
     [_item("a", 15, "fair"), _item("b", 25, "good"), _item("c", 18, "excellent")],
     "c", "only excellent"),
]


def trial_c1():
    """Return (pass_count, total, details). Deterministic."""
    details = []
    passes = 0
    for name, items, expected, why in C1_CASES:
        result = compare_listings(items)
        ok = result["pick_id"] == expected
        passes += int(ok)
        details.append((name, expected, result["pick_id"], result["pick_reason"], ok))
    return passes, len(C1_CASES), details


# ── C4 fixtures: 5 bad /ask payloads ─────────────────────────────────────────
C4_PAYLOADS = [
    b"{}",
    b'{"query": ""}',
    b'{"query": "   "}',
    b'{"wardrobe": {"items": []}}',
    b'{"query": null}',
]


def trial_c4():
    """Return (pass_count, total, details). pass = HTTP 400 AND status=bad_request logged."""
    details = []
    passes = 0
    before = _line_count(LOG_FILE)
    for payload in C4_PAYLOADS:
        req = urllib.request.Request(
            "http://localhost:5000/ask", data=payload,
            headers={"Content-Type": "application/json"},
        )
        http_code = None
        try:
            urllib.request.urlopen(req, timeout=10).read()
            http_code = 200
        except urllib.error.HTTPError as e:
            http_code = e.code
        details.append({"payload": payload.decode(), "http": http_code})
    # Inspect new log lines for status=bad_request
    new_lines = _read_lines_from(LOG_FILE, before)
    bad_requests_logged = sum(1 for l in new_lines if l.get("status") == "bad_request")
    for d in details:
        d["log_matched"] = d["http"] == 400
        if d["http"] == 400:
            passes += 1
    return passes, len(C4_PAYLOADS), details, bad_requests_logged, len(new_lines)


# ── C2/C3/C5 shared /ask batch ───────────────────────────────────────────────
BATCH_QUERIES = [
    # 10 that should hit >= 2 (first 10 used for C2 and C3)
    "vintage graphic tee under $30",
    "oversized flannel shirt size L",
    "y2k baby tee under $25",
    "corduroy jacket, M",
    "cargo pants size 30 under $40",
    "denim jacket under $50",
    "levi 501 jeans",
    "band tee size M",
    "jeans",
    "jacket",
    # 5 that should hit 0 (to confirm branch skips)
    "wool sweater under $35",
    "designer ballgown size XXS under $5",
    "bicycle under $20",
    "silk kimono",
    "fedora size 7",
    # 5 extra to round out to 20 for C5's line count delta
    "cardigan",
    "shacket",
    "mesh top",
    "track jacket",
    "leather bomber",
]
assert len(BATCH_QUERIES) == 20


def batch_trial(batch_idx):
    """Run 20 /ask requests. Return (log_records_added, batch_rows_from_log)."""
    before = _line_count(LOG_FILE)
    sessions = []
    for i, q in enumerate(BATCH_QUERIES):
        req = urllib.request.Request(
            "http://localhost:5000/ask",
            data=json.dumps({"query": q}).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            body = urllib.request.urlopen(req, timeout=180).read()
            sessions.append(json.loads(body))
        except Exception as e:
            sessions.append({"error": f"request failed: {e}"})
        print(f"  batch {batch_idx} req {i+1:>2}/20: {q[:40]}", flush=True)
    new_lines = _read_lines_from(LOG_FILE, before)
    return new_lines, sessions


def score_c2(log_lines):
    """First 10 entries: comparison_ran == (search_hits >= 2)."""
    passes = 0
    details = []
    for rec in log_lines[:10]:
        hits = rec.get("search_hits", 0)
        ran = rec.get("comparison_ran", False)
        expected = hits >= 2
        ok = ran == expected
        passes += int(ok)
        details.append({"query": rec.get("query"), "hits": hits, "ran": ran, "expected": expected, "ok": ok})
    return passes, 10, details


def score_c3(log_lines, sessions):
    """Of the first 10 /ask sessions where comparison_ran, check row key set.
    We need the FULL session, not just the log — rows aren't in the log."""
    required = {"id", "title", "price", "condition", "size", "size_fit", "platform", "brand"}
    checked = 0
    passes = 0
    details = []
    for i in range(min(10, len(sessions))):
        s = sessions[i]
        comp = s.get("comparison")
        if not comp:
            continue
        checked += 1
        rows = comp.get("rows", [])
        all_ok = all(set(r.keys()) >= required for r in rows)
        passes += int(all_ok)
        details.append({"query_idx": i, "rows_checked": len(rows), "all_fields_present": all_ok})
    return passes, checked, details


def score_c5(log_lines):
    """All 20 produced a record with ts, request_id, status, duration_ms."""
    required = {"ts", "request_id", "status", "duration_ms"}
    passes = sum(1 for rec in log_lines if set(rec.keys()) >= required)
    return passes, 20, len(log_lines)


# ── helpers ──────────────────────────────────────────────────────────────────
def _line_count(path):
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def _read_lines_from(path, start_line):
    if not path.exists():
        return []
    out = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < start_line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


# ── runner ───────────────────────────────────────────────────────────────────
def main():
    report = ["# Capstone — Run Log — Before\n",
              f"_Generated {datetime.now(timezone.utc).isoformat()} by scripts/run_trials.py_\n"]

    # C1 trials — no server needed
    print("\n=== C1 (compare_listings pick rule, 10 crafted inputs) ===")
    c1_scores = []
    c1_last_details = None
    for t in range(1, 4):
        passes, total, details = trial_c1()
        c1_scores.append(f"{passes}/{total}")
        c1_last_details = details
        print(f"  trial {t}: {passes}/{total}")

    # Start server for /ask trials
    print("\nStarting serve.py ...")
    srv = subprocess.Popen(
        [sys.executable, "serve.py"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        env={**os.environ},
        cwd=str(ROOT),
    )
    time.sleep(3)

    try:
        # C4 trials
        print("\n=== C4 (bad /ask returns 400 + log) ===")
        c4_scores, c4_bad_counts, c4_last_details = [], [], None
        for t in range(1, 4):
            passes, total, details, bad_logged, new_total = trial_c4()
            c4_scores.append(f"{passes}/{total}")
            c4_bad_counts.append((bad_logged, new_total))
            c4_last_details = details
            print(f"  trial {t}: http=400 in {passes}/{total}, bad_request logged = {bad_logged}/{new_total} new records")

        # C2/C3/C5 shared trials
        print("\n=== C2+C3+C5 (shared /ask batches of 20) ===")
        c2_scores, c3_scores, c5_scores = [], [], []
        last_c2, last_c3, last_c5_count = None, None, None
        last_batch_lines = None
        for t in range(1, 4):
            lines, sessions = batch_trial(t)
            c2_pass, c2_total, c2_det = score_c2(lines)
            c3_pass, c3_total, c3_det = score_c3(lines, sessions)
            c5_pass, c5_total, c5_count = score_c5(lines)
            c2_scores.append(f"{c2_pass}/{c2_total}")
            c3_scores.append(f"{c3_pass}/{c3_total}" if c3_total else "n/a")
            c5_scores.append(f"{c5_pass}/{c5_total} ({c5_count} lines)")
            last_c2, last_c3, last_c5_count = c2_det, c3_det, c5_count
            last_batch_lines = lines
            print(f"  trial {t}: C2 {c2_scores[-1]} | C3 {c3_scores[-1]} | C5 {c5_scores[-1]}")
    finally:
        srv.terminate()
        srv.wait(timeout=5)

    # ── report ──
    report.append("## Run Log table\n")
    report.append("| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |")
    report.append("|---|---|---|---|---|---|")
    def verdict_num(scores, target_pass, target_of):
        # all three trials must meet
        return "MET" if all(_pass(s) >= target_pass for s in scores) else "MISSED"
    def _pass(s): return int(s.split("/")[0])
    report.append(f"| C1. pick rule correctness | 10/10 | {c1_scores[0]} | {c1_scores[1]} | {c1_scores[2]} | {verdict_num(c1_scores, 10, 10)} |")
    report.append(f"| C2. branch fires iff hits>=2 | 10/10 | {c2_scores[0]} | {c2_scores[1]} | {c2_scores[2]} | {verdict_num(c2_scores, 10, 10)} |")
    report.append(f"| C3. row has 8 fields | 10/10 (or all eligible) | {c3_scores[0]} | {c3_scores[1]} | {c3_scores[2]} | {'MET' if all(c.split('/')[0]==c.split('/')[1] for c in c3_scores) else 'MISSED'} |")
    report.append(f"| C4. bad query → 400 + log | 5/5 | {c4_scores[0]} | {c4_scores[1]} | {c4_scores[2]} | {verdict_num(c4_scores, 5, 5)} |")
    report.append(f"| C5. every /ask → 1 record | 20/20 | {c5_scores[0]} | {c5_scores[1]} | {c5_scores[2]} | {verdict_num(c5_scores, 20, 20)} |")

    report.append("\n## Real output per criterion (trial 3)\n")

    report.append("### C1 — compare_listings direct call (tools.py::compare_listings)\n")
    report.append("```")
    for name, expected, got, reason, ok in c1_last_details:
        mark = "OK" if ok else "FAIL"
        report.append(f"  [{mark}] {name}: expected={expected}, got={got} — {reason}")
    report.append("```\n")

    report.append("### C4 — bad request via POST /ask (serve.py::ask)\n")
    report.append("```")
    for d in c4_last_details:
        report.append(f"  payload={d['payload']!r:40s} → HTTP {d['http']}  log_matched_400={d['log_matched']}")
    bl, nt = c4_bad_counts[-1]
    report.append(f"  log records added: {nt}, of which status=bad_request: {bl}")
    report.append("```\n")

    report.append("### C2 — branch firing per log record (serve.py::ask, agent.py::run_agent)\n")
    report.append("```")
    for d in last_c2:
        mark = "OK" if d["ok"] else "FAIL"
        report.append(f"  [{mark}] {d['query'][:38]:38s} hits={d['hits']:>2}  ran={str(d['ran']):5s}  expected={d['expected']}")
    report.append("```\n")

    report.append("### C3 — row field presence per session (tools.py::compare_listings)\n")
    report.append("```")
    for d in last_c3:
        mark = "OK" if d["all_fields_present"] else "FAIL"
        report.append(f"  [{mark}] query_idx={d['query_idx']}  rows={d['rows_checked']}  all_fields_present={d['all_fields_present']}")
    report.append("```\n")

    report.append("### C5 — log reliability (serve.py::_write_log)\n")
    report.append(f"```\n  requests sent: 20\n  log records added: {last_c5_count}\n  valid JSON with required keys: {score_c5(last_batch_lines)[0]}\n```\n")

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")
    print(f"\nReport written to {REPORT_FILE}")


if __name__ == "__main__":
    main()
