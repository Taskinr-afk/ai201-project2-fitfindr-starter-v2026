# Capstone — Run Log — Before

_Generated 2026-11-15T00:35:32.842108+00:00 by scripts/run_trials.py_

## Run Log table

| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |
|---|---|---|---|---|---|
| C1. pick rule correctness | 10/10 | 10/10 | 10/10 | 10/10 | MET |
| C2. branch fires iff hits>=2 | 10/10 | 10/10 | 10/10 | 10/10 | MET |
| C3. row has 8 fields | 10/10 (or all eligible) | 10/10 | 10/10 | 10/10 | MET |
| C4. bad query → 400 + log | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| C5. every /ask → 1 record | 20/20 | 20/20 (20 lines) | 20/20 (20 lines) | 20/20 (20 lines) | MET |

## Real output per criterion (trial 3)

### C1 — compare_listings direct call (tools.py::compare_listings)

```
  [OK] single excellent wins: expected=b, got=b — only excellent option at $20
  [OK] cheapest of two excellents: expected=b, got=b — cheapest among excellent options at $20
  [OK] tie on cond+price picks first: expected=a, got=a — tied on condition (excellent) and price ($20); top search match
  [OK] all same tier, cheapest wins: expected=b, got=b — cheapest among good options at $15
  [OK] all fair, pick cheapest: expected=b, got=b — cheapest among fair options at $10
  [OK] excellent beats cheaper good: expected=b, got=b — only excellent option at $50
  [OK] 3 goods, middle price: expected=b, got=b — cheapest among good options at $20
  [OK] excellent at same price as good: expected=b, got=b — only excellent option at $20
  [OK] two excellent, one much cheaper: expected=b, got=b — cheapest among excellent options at $10
  [OK] mixed; cheapest-excellent at pos 3: expected=c, got=c — only excellent option at $18
```

### C4 — bad request via POST /ask (serve.py::ask)

```
  payload='{}'                                     → HTTP 400  log_matched_400=True
  payload='{"query": ""}'                          → HTTP 400  log_matched_400=True
  payload='{"query": "   "}'                       → HTTP 400  log_matched_400=True
  payload='{"wardrobe": {"items": []}}'            → HTTP 400  log_matched_400=True
  payload='{"query": null}'                        → HTTP 400  log_matched_400=True
  log records added: 5, of which status=bad_request: 5
```

### C2 — branch firing per log record (serve.py::ask, agent.py::run_agent)

Re-scored across a MIX of hit counts (indices 0,2,4,6,8 + 10..14 from the batch of 20) via scripts/rescore_c2.py. The original run_trials.py scoring only looked at the first 10, which were all many-hit — honest to add the zero-hit observations too.

```
  [OK] vintage graphic tee under $30          hits=10  ran=True   expected=True
  [OK] y2k baby tee under $25                 hits= 5  ran=True   expected=True
  [OK] cargo pants size 30 under $40          hits= 5  ran=True   expected=True
  [OK] levi 501 jeans                         hits= 3  ran=True   expected=True
  [OK] jeans                                  hits= 3  ran=True   expected=True
  [OK] wool sweater under $35                 hits= 0  ran=False  expected=False
  [OK] designer ballgown size XXS under $5    hits= 0  ran=False  expected=False
  [OK] bicycle under $20                      hits= 0  ran=False  expected=False
  [OK] silk kimono                            hits= 2  ran=True   expected=True
  [OK] fedora size 7                          hits= 5  ran=True   expected=True
```

### C3 — row field presence per session (tools.py::compare_listings)

```
  [OK] query_idx=0  rows=3  all_fields_present=True
  [OK] query_idx=1  rows=3  all_fields_present=True
  [OK] query_idx=2  rows=3  all_fields_present=True
  [OK] query_idx=3  rows=3  all_fields_present=True
  [OK] query_idx=4  rows=3  all_fields_present=True
  [OK] query_idx=5  rows=3  all_fields_present=True
  [OK] query_idx=6  rows=3  all_fields_present=True
  [OK] query_idx=7  rows=2  all_fields_present=True
  [OK] query_idx=8  rows=3  all_fields_present=True
  [OK] query_idx=9  rows=3  all_fields_present=True
```

### C5 — log reliability (serve.py::_write_log)

```
  requests sent: 20
  log records added: 20
  valid JSON with required keys: 20
```
