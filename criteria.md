# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

---

## 3. Something about state

The item in session["selected_item"] matches the item that actually reaches suggest_outfit, checked by id, and this holds in 5 of 5 tries.

**Why this target:**

The two tool calls never touch each other directly, everything passes through the session in between, and if the id drifts from one step to the next, the session has failed at its one job, so this should hold every time and not just most times.

---

## 4. Something about the fit card

The fit card names the item's price at least once, in 5 of 5 tries.

**Why this target:**

The price is a fact pulled straight from the listing rather than a creative choice, and while the wording can change every run, the price itself should never go missing, since a caption without it is dropped detail, not stylistic variation.

---

## 5. Your choice

When max_price is set, every listing search_listings returns is at or under that price, across 10 different queries.

**Why this target:**

The price ceiling is a hard filter rather than something the model can round on its own, so even one listing over budget means the filter is broken, which is why this one gets checked across more tries than the others.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria

Written in Unit 9 Milestone 4, before any trial runs for the capstone existed.
Three are about the new `compare_listings` tool and the branch that calls it.
One is about the bad path. One is about the instrumentation that Milestone 3
put around the system.

## 1. compare_listings picks by the documented rule (extension)

Given 10 crafted input sets where the ground-truth pick is known — a mix of
(a) one item at a better condition than the others, (b) two or more items
tied on the top condition tier at different prices, and (c) all items at the
same condition and price — `compare_listings` returns the expected item as
`pick_id` in 10 of 10 cases.

**Target:** 10 / 10

**Why this target:** The pick rule is pure data — no model call, no
randomness. Condition rank is a three-element lookup, price is a float
compare, ties break on input order. Any miss means the rule in tools.py does
not match the code, and `suggest_outfit` is building an outfit around the
wrong item. One wrong pick in the sample is enough to show that.

## 2. The branch fires if and only if search returned at least two listings (extension)

Across 10 `/ask` requests covering a mix of 0-hit, 1-hit, 2-hit and many-hit
searches, `session["comparison"]` is a dict when `search_hits >= 2` and is
`None` when `search_hits < 2`. 10 of 10.

**Target:** 10 / 10

**Why this target:** This is the rule I wrote into the loop in Milestone 1.
It is a single if-statement with no model call, so correctness is either 100
percent or it is a bug. Anything less means the loop is doing something other
than what the README Shape paragraph claims.

## 3. Every comparison row carries all eight fields (extension)

Every row in `session["comparison"]["rows"]` contains the keys `id`, `title`,
`price`, `condition`, `size`, `size_fit`, `platform`, `brand`. `brand` may be
`null` because the data has unbranded listings, but the key must be present.
Checked across 10 `/ask` runs whose `search_hits >= 2`.

**Target:** 10 / 10

**Why this target:** A missing field in a comparison row is a silent change
to the tool's contract — downstream code that reads rows will see `None`
instead of raising `KeyError`, which is the harder bug to find later. The
fields are set by a dict literal in `compare_listings`, so the only way this
fails is a code edit that forgets a key. That is exactly the regression a
criterion should catch.

## 4. A missing query returns HTTP 400 and writes a log record (bad path)

`POST /ask` with body `{}` or body `{"query": ""}` returns HTTP 400 with a
JSON body naming the missing field, AND appends one record to
`logs/requests.jsonl` with `status: "bad_request"`. Both halves must hold in
5 of 5 attempts.

**Target:** 5 / 5

**Why this target:** 5 of 5, not 4 of 5, because this is a pure code path
with no model call and no network — there is no reason for intermittent
failure. The log half matters as much as the HTTP half: a 400 without a log
entry is a failure that leaves no record, which defeats the whole point of
the instrumentation work in Milestone 3.

> **Tightened in Milestone 6 as "The Improvement" target.** 5 / 5 was met on
> three trials, so the original target was too narrow — it only exercised
> the missing/empty-query branch I had already coded for. A real "bad path"
> criterion has to cover ill-typed inputs the handler never sees in normal
> use, since those are where a 400 turns into an accidental 500.
>
> **Tightened target:** across 10 payload variants (the original 5 plus 5
> ill-typed ones: `query` as list, number, bool, dict, and a request with no
> `Content-Type: application/json` header), every request returns HTTP 400
> AND writes a `status: "bad_request"` record. 10 / 10 across 3 trials.
>
> This isn't a revision because the original was broken — the original was
> MET. The tightening is listed here so the Milestone 6 improvement has a
> written target to hit.

## 5. Every /ask request produces exactly one log record (observability)

Across 20 `/ask` requests (a mix of `ok`, `no_match`, and `bad_request`),
the line count of `logs/requests.jsonl` increases by exactly 20, and each new
line parses as valid JSON containing at minimum `ts`, `request_id`, `status`,
and `duration_ms`.

**Target:** 20 / 20

**Why this target:** The log is the only record of a run after the process
exits. A dropped line is a run I cannot diagnose; a doubled line is one I
would double-count in any metric built on it. The writer is a plain append
under a lock, so the behaviour is meant to be exact. Milestone 5 cannot
verify anything else about the system without this holding first, if the
log is unreliable, every other criterion built on reading it is unreliable
too.

