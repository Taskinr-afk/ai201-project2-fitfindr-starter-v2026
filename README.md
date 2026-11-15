# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

A user describes an item they want, in plain language, with an optional size and price limit, like "vintage graphic tee under $30, size M". FitFindr searches a set of secondhand listings for the best match, then looks at the user's existing wardrobe and suggests an outfit built around that item. It finishes by writing a short caption the user could post about the find. If nothing in the listings matches, FitFindr stops there and tells the user what to change about their search, instead of guessing.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Takes the user's description and finds the listings that match it. Any listing over the price limit is dropped first. Any listing in the wrong size is dropped next. Each listing left gets a score for how many of the user's words show up in it. The search looks at the title as well as the description and the style tags.
- **Inputs:** description (str), size (str or None), max_price (float or None).
- **Returns:** A list of listing dicts with the best score first. The list holds at most 10 listings. Each dict has id, title, description, category, style_tags, size, condition, price, colors, brand and platform.
- **When it has nothing:** An empty list. It never returns None and it never causes an error.

### `suggest_outfit`

- **What it does:** It takes a thrifted item and the user's wardrobe. It asks the model for one or two outfit ideas. If the wardrobe is empty, it asks for general styling advice instead.
- **Inputs:** new_item (dict), wardrobe (dict with an items key holding a list).
- **Returns:** A string with the model's outfit suggestion.
- **When it has nothing:** With an empty wardrobe it still gives back a full string of general styling advice. It never returns an empty string. It never causes an error.

### `create_fit_card`

- **What it does:** It writes a short caption someone could actually post about the find. It uses the outfit suggestion plus the item's price and platform.
- **Inputs:** outfit (str), new_item (dict).
- **Returns:** A string, two to four sentences long, written like a real post rather than a product listing.
- **When it has nothing:** If outfit is empty or only whitespace, it returns a message saying there is no outfit to caption. It does not cause an error.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, put a message in session["error"] that tells the user what to change about their search. Then stop. Otherwise take the first result as session["selected_item"] and move on to suggest_outfit.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** regex.

**What moves through the session:** query first, then parsed holding description, size and max_price, then search_results, then selected_item, then outfit_suggestion, then fit_card. If the loop stops early, error gets set and the rest stay None.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30, size M'
  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two ways to style the Y2K butterfly baby tee using pieces already in your wardrobe, leaning into that authentic early 2000s aesthetic:

**Outfit 1: The Classic Y2K Streetwear Look**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* Pairing the fitted, cropped silhouette of the baby tee with baggy, dark-wash denim creates the quintessential Y2K proportion play. Tossing the vintage black denim jacket over top keeps the color palette grounded while adding an effortless, grunge-leaning edge, finished off with chunky sneakers and a crossbody.

**Outfit 2: Casual Retro-Prep**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Shoes:** Chunky white sneakers (or Black combat boots, depending on the vibe)
*   *Why it works:* Tucking the baby tee into the wide-leg khaki trousers highlights your waist while playing with looser tailoring on the bottom. Add the brown leather belt to tie the earthy khaki tones together, and finish with chunky white sneakers for a fresh, everyday retro look.

  Fit card: Obsessed with the nostalgic colorway on this Y2K butterfly baby tee! It's giving major early 2000s mall-goth energy and I'm honestly tempted to keep it. Grab it on my Depop right now for just $18 before I change my mind.

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two outfit ideas that pair the vintage Levi's 501 jeans with items already in the wardrobe:

**Outfit 1: Casual & Effortless**
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* The medium-wash Levi's and the white ribbed tank create a classic, timeless base. Tossing on the black denim jacket adds a cool double-denim contrast, while the chunky white sneakers and black crossbody keep the look relaxed and modern for daytime wear.

**Outfit 2: Edgy & Cozy**
*   **Top:** Oversized grey crewneck sweatshirt
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, Black crossbody bag
*   *Why it works:* Tucking the medium-wash 501s into the brown leather belt adds a touch of definition before layering the oversized grey crewneck over top (you could do a casual half-tuck). Paired with the black combat boots, this look leans into the vintage, slightly rugged aesthetic of the jeans while staying comfortable and grounded.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the vintage fade on these classic Levi's 501 jeans. Just throw them on with some fresh white sneakers for that effortless model-off-duty vibe. Grab this medium wash pair for $38.0 on depop before I change my mind and keep them!
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* A function that pulls a description, a size, and a price ceiling out of a plain language query like "vintage graphic tee under $30, size M", using regex only.
- *What came back:* A working version that matched prices after words like "under" or "below", and size either from a phrase like "size M" or a bare size word found anywhere in the sentence.
- *What I changed:* Later in the unit I got the professor's finished agent.py, and his parser handled a few things more carefully than mine, matching a trailing bare size only at the end of a sentence instead of anywhere, and matching a price right after a dollar sign rather than needing a word like "under" in front of it. I swapped his version in over mine once I saw the difference.

**Moment 2**

- *What I asked for:* To test suggest_outfit and create_fit_card from a terminal, calling the model for real.
- *What came back:* A ModuleNotFoundError, no module named google, instead of a real response.
- *What I changed:* I checked the repo for a virtual environment, found .venv already set up at the root, and reran the same test through that interpreter instead of plain python. It worked immediately once the right environment was used.

**Moment 3**

- *What I asked for:* Help identifying what to improve after all five criteria already passed. I needed something measurable to change and rerun.
- *What came back:* A suggestion to fix the price formatting in create_fit_card, where raw floats like 18.0 showed up as "$18.0" in fit cards instead of "$18". The fix was adding :g to the format string.
- *What I changed:* Nothing really about the fix itself, since the diagnosis was right and the one line change worked on the first try. The after run confirmed zero trailing zeros across all fit cards.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item in session matches item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every returned listing is at or under max_price | 10 of 10 | PASS | PASS | PASS | PASS | PASS | MET (10/10) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Criterion 1** — `run_eval.py::run_once`, query: `vintage graphic tee under $30`

```
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:
Found my ultimate Y2K holy grail and I'm honestly so tempted to keep it. This adorable butterfly baby tee is giving major early-2000s pop star off-duty vibes. Snagged it on Depop for just $18, but check out my page to grab it before I change my mind!
```

**Criterion 2** — `run_eval.py::run_once`, query: `designer ballgown size XXS under $5`

```
- stopped early: yes — Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
- selected_item: (none)
- search_results: 0
```

**Criterion 3** — `run_eval.py::run_once`, query: `vintage graphic tee under $30`

```
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Trace:
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
```

The selected_item id (lst_002) is the same item that reaches suggest_outfit, confirmed by the trace showing the same title passed in.

**Criterion 4** — `run_eval.py::run_once`, query: `vintage graphic tee under $30`

```
Fit card:
Obsessed with the pink and purple print on this Y2K butterfly baby tee. It's giving major early-2000s mall goth energy, and I'm listing it on Depop for just $18. Grab it before I change my mind and keep it for myself!
```

The price $18 appears in the fit card.

**Criterion 5** — `run_eval.py::run_once`, 10 budget filter queries

All 10 queries returned only listings at or under their max_price. Two queries (wool sweater under $40 and crossbody bag under $30) returned empty results, which still satisfies the criterion since no over-budget listing was returned. The other eight returned items priced at $18, $42, $55, $30, $20, $30, $32, and $30, all under their respective ceilings of $30, $50, $60, $35, $45, $50, $35, and $40.

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | All five tries returned a fit card with no crashes or early stops. |
| 2 | Impossible query stops before tool 2 | 5 of 5 | MET (5/5) | All five tries set session["error"] and returned before calling suggest_outfit, confirmed by the trace stopping at step 3. |
| 3 | Item in session matches item passed on | 5 of 5 | MET (5/5) | In every try the trace shows the same item title at select_item and at the input to suggest_outfit. |
| 4 | Fit card mentions the item's price | 5 of 5 | MET (5/5) | Searched each fit card for the string "$18" and found it in all five. |
| 5 | Every returned listing is at or under max_price | 10 of 10 | MET (10/10) | Checked the selected item price against the ceiling for each of the 10 queries. Two queries returned empty results which still satisfies the filter since nothing over budget came back. |

**Diagnoses**

None of the criteria was missed. The targets were probably set on the easy side. Criteria 1 through 3 tested the deterministic behavior since search_listings is keyword matching with no model call, so the same query always picks the same item and the branch always fires the same way. The only criteria that depend on the model are 4 and 5, and criterion 4 passed because the prompt for create_fit_card explicitly hands the price to the model as a fact to include. Criterion 5 does not involve the model at all since search_listings filters by price before scoring.

The criterion I would tighten is criterion 1. Right now it just checks that the agent finishes without crashing. A harder version would check that the outfit suggestion actually names at least one item from the wardrobe, which would test whether suggest_outfit is using the wardrobe data rather than making something up.


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] parse_query
      in:  Find me a vintage graphic tee under 30 dollars in size medium
      out: {'description': 'Find me a vintage graphic tee under 30 dollars in size medium', 'size': None, 'max_price': None}
[2] search_listings (via MCP)
      in:  {'description': 'Find me a vintage graphic tee under 30 dollars in size medium', 'size': None, 'max_price': None}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Mesh Long-Sleeve Top — Black … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Here are two ways to style the Y2K butterfly baby tee using pieces already in your wardrobe…
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Found the absolute cutest Y2K baby tee with the dreamiest butterfly print for only $18!…
```

**Empty search**

```
[1] parse_query
      in:  Find me a cashmere tuxedo under 5 dollars
      out: {'description': 'Find me a cashmere tuxedo under 5 dollars', 'size': None, 'max_price': None}
[2] search_listings (via MCP)
      in:  {'description': 'Find me a cashmere tuxedo under 5 dollars', 'size': None, 'max_price': None}
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

In Milestone 1 I moved search_listings out of agent.py and onto an MCP server in mcp_server.py. The server registers the same function with the same typed inputs using FastMCP. In agent.py the direct call `search_listings(description, size, max_price)` was replaced with `call_tool("search_listings", {...})` from mcp_client.py. The results came back the same as before. The trace above shows "via MCP" on step 2, confirming the call goes through the server now.


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** In create_fit_card in tools.py, changed the price format string from `${new_item['price']}` to `${new_item['price']:g}`. The `:g` format strips any of the trailing zeros so the model sees "$18" instead of "$18.0" in its prompt.

**Which failure it was meant to fix:** Not a failure against the criteria, since all five MET. The diagnosis said the targets were easy and the model facing parts were the only place anything could drift. In the before run, some fit cards wrote the price as "$18.0" or "$55.0" instead of "$18" or "$55" because the prompt handed the raw float to the model. The trailing zero is not wrong but it looked pretty much like a bug when I started encountering it alot. 

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item in session matches item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every returned listing is at or under max_price | 10 of 10 | PASS | PASS | PASS | PASS | PASS | MET (10/10) |

**Did it help, and how do I know:**

Yes, in the before run, several fit cards wrote the price with a trailing zero like "$18.0" or "$55.0". In the after run, every fit card across all tries writes clean prices like "$18", "$42", "$55", "$30", "$20", and "$32". The change did not affect any criterion verdict since all five already MET, but it fixed the formatting issue the diagnosis identified.



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

None of the criteria were missed. and all five met their targets in both the before and after runs. If I were to raise the bar, criterion 1 would be the first to test at a harder target since parse_query does not extract size or max_price from every phrasing. The query "vintage graphic tee under 30 dollars in size medium" returned size as None and max_price as None, meaning the parser missed both filters. The results still matched because keyword scoring happened to rank the right items, but I think a stricter criterion that checked whether the filters were actually applied would fail.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

## Capstone

**What This Extends**
FitFindr, my Unit 3/4 project. The three existing tools stay as they are. I'm adding a fourth tool, compare_listings, and one new branch in the planning loop that calls it when search returns two or more hits.

**The Shape**
I chose Shape C, which extends one capability. compare_listings takes 2-3 listings from search_listings and returns a side-by-side comparison on price, condition, size fit, and a short reason for the pick. The agent calls it after search_listings when there are at least two results, before suggest_outfit. With one result or none, the loop skips it and behaves exactly as it did before.

Out of scope:
1. No changes to search_listings ranking, the size parser, or the price regex.
2. No changes to suggest_outfit or create_fit_card.
3. No image comparison and no fetching external listing data.
4. compare_listings stays a plain function in tools.py — not exposed over MCP. Keeps it a pure function over data the agent already has.
5. No UI changes to app.py beyond printing the comparison when it runs.

**Running It**
Path B — local with logs. The full start command and environment are in [RUNNING.md](RUNNING.md) under the Capstone section. One command: `python serve.py`. Server binds `http://localhost:5000`, one request at a time.

**Instrumentation**
Every `/ask` request writes one JSON record to `logs/requests.jsonl`, appended. Failures write records too — a 400 for a missing query and a 500 for an agent exception. Fields per record:

- `ts` — ISO-8601 UTC timestamp
- `request_id` — 8-char uuid4 prefix
- `query` — the raw user query string
- `status` — `ok`, `no_match`, `bad_request`, or `error`
- `http` — HTTP status code returned
- `duration_ms` — end-to-end wall time, including the queue wait
- `search_hits` — how many listings search_listings returned
- `comparison_ran` — true when `len(results) >= 2` triggered the new branch
- `pick_reason` — the string compare_listings used to explain its pick
- `selected_item_id` — the listing id handed to suggest_outfit
- `prompt_tokens` / `output_tokens` — per-request delta from `generate.token_counts()`
- `error` — the error message when not null

Eleven entries from one session (10 /ask runs plus 1 rejected request):

```
[01] {"ts": "2026-11-15T00:05:24.142854+00:00", "request_id": "a05c81d3", "query": "", "status": "bad_request", "http": 400, "duration_ms": 0.4, "error": "missing or empty query field"}

[02] {"ts": "2026-11-15T00:05:26.211339+00:00", "request_id": "9b9cdf31", "query": "vintage graphic tee under $30", "status": "ok", "http": 200, "duration_ms": 7533.8, "search_hits": 10, "comparison_ran": true, "pick_reason": "only excellent option at $18", "selected_item_id": "lst_002", "prompt_tokens": 649, "output_tokens": 407, "error": null}

[03] {"ts": "2026-11-15T00:05:35.797382+00:00", "request_id": "c6bee6b1", "query": "oversized flannel shirt size L", "status": "ok", "http": 200, "duration_ms": 4390.0, "search_hits": 3, "comparison_ran": true, "pick_reason": "cheapest among excellent options at $17", "selected_item_id": "lst_040", "prompt_tokens": 618, "output_tokens": 363, "error": null}

[04] {"ts": "2026-11-15T00:05:42.251183+00:00", "request_id": "4b2fa6b9", "query": "y2k baby tee under $25", "status": "ok", "http": 200, "duration_ms": 3916.3, "search_hits": 5, "comparison_ran": true, "pick_reason": "cheapest among excellent options at $15", "selected_item_id": "lst_017", "prompt_tokens": 504, "output_tokens": 247, "error": null}

[05] {"ts": "2026-11-15T00:05:48.231708+00:00", "request_id": "4feaec61", "query": "corduroy jacket, M", "status": "ok", "http": 200, "duration_ms": 4173.6, "search_hits": 3, "comparison_ran": true, "pick_reason": "cheapest among excellent options at $33", "selected_item_id": "lst_032", "prompt_tokens": 594, "output_tokens": 351, "error": null}

[06] {"ts": "2026-11-15T00:05:54.457006+00:00", "request_id": "775d8bf7", "query": "cargo pants size 30 under $40", "status": "ok", "http": 200, "duration_ms": 4106.2, "search_hits": 5, "comparison_ran": true, "pick_reason": "only excellent option at $15", "selected_item_id": "lst_017", "prompt_tokens": 590, "output_tokens": 347, "error": null}

[07] {"ts": "2026-11-15T00:06:00.615567+00:00", "request_id": "0342d1a0", "query": "denim jacket under $50", "status": "ok", "http": 200, "duration_ms": 4184.9, "search_hits": 7, "comparison_ran": true, "pick_reason": "cheapest among excellent options at $42", "selected_item_id": "lst_007", "prompt_tokens": 605, "output_tokens": 340, "error": null}

[08] {"ts": "2026-11-15T00:06:06.896091+00:00", "request_id": "ba001101", "query": "levi 501 jeans", "status": "ok", "http": 200, "duration_ms": 4351.5, "search_hits": 3, "comparison_ran": true, "pick_reason": "cheapest among good options at $30", "selected_item_id": "lst_037", "prompt_tokens": 599, "output_tokens": 364, "error": null}

[09] {"ts": "2026-11-15T00:06:13.322175+00:00", "request_id": "262486fa", "query": "band tee size M", "status": "ok", "http": 200, "duration_ms": 19162.3, "search_hits": 2, "comparison_ran": true, "pick_reason": "cheapest among excellent options at $15", "selected_item_id": "lst_017", "prompt_tokens": 591, "output_tokens": 358, "error": null}

[10] {"ts": "2026-11-15T00:06:34.542710+00:00", "request_id": "1c46c65f", "query": "wool sweater under $35", "status": "no_match", "http": 200, "duration_ms": 2308.4, "search_hits": 0, "comparison_ran": false, "pick_reason": null, "selected_item_id": null, "prompt_tokens": 0, "output_tokens": 0, "error": "Nothing in the listings matched description 'wool sweater', under $35. Things to change: try broader words; raise the price ceiling above $35."}

[11] {"ts": "2026-11-15T00:06:38.908809+00:00", "request_id": "2f73e35a", "query": "designer ballgown size XXS under $5", "status": "no_match", "http": 200, "duration_ms": 2426.9, "search_hits": 0, "comparison_ran": false, "pick_reason": null, "selected_item_id": null, "prompt_tokens": 0, "output_tokens": 0, "error": "Nothing in the listings matched description 'designer ballgown', size XXS, under $5. Things to change: try broader words; drop the size; raise the price ceiling above $5."}
```

Two failure shapes are visible in the log: `bad_request` (http 400, no query field) and `no_match` (http 200, search returned zero hits, no model calls made so tokens are 0).

**What It Costs**
$0.00020 per run, measured.

Method: `scripts/measure_cost.py` runs the agent 10 times with `AI201_CACHE=0` (so every call actually hits the model), captures per-run tokens via `generate.token_counts()` deltas, times each run with `time.perf_counter()`. The dollar figure uses the published Gemini 3.5 Flash-Lite rate ($0.10 per 1M input tokens, $0.40 per 1M output). Tokens are measured; the rate is the only thing published pricing lets you multiply measured tokens by.

Averages over 10 runs:

- Wall time: 7.59 s (one run hit the model's per-minute rate limit and waited 27s — that drags the mean; median was closer to 4.4 s)
- Prompt tokens: 609.4
- Output tokens: 356.7
- $ per run: $0.00020
- $ per 100 runs/day: $0.00020 × 100 = **$0.0204/day**, or roughly 2 cents a day for a hundred people. At 100/day for a year, that's $7.44 in API spend.

**Run Log and Verdicts**
Produced by `scripts/run_trials.py` on 2026-11-15, with C2 re-scored across a proper mix of hit counts by `scripts/rescore_c2.py`. Full report in [results/capstone_before.md](results/capstone_before.md).

| # | Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |
|---|---|---|---|---|---|---|
| C1 | compare_listings picks by documented rule | 10/10 | 10/10 | 10/10 | 10/10 | MET |
| C2 | Branch fires iff `search_hits >= 2` | 10/10 (mixed hit counts) | 10/10 | 10/10 | 10/10 | MET |
| C3 | Every comparison row has all 8 fields | 10/10 of eligible | 10/10 | 10/10 | 10/10 | MET |
| C4 | Missing query → HTTP 400 + log record | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| C5 | Every /ask → exactly one valid log record | 20/20 | 20/20 | 20/20 | 20/20 | MET |

Verdict summary: **5/5 MET, no misses to diagnose.** This is honest but uncomfortable — see **What's Still Broken** and **The Improvement** below for the target I'd tighten and the improvement I ran against the tightened target.

Real output from trial 3, one block per criterion. All are produced by the test harness and pasted verbatim from `results/capstone_before.md`.

**C1 — `tools.py::compare_listings` called directly on 10 crafted inputs**
```
  [OK] single excellent wins:                expected=b, got=b — only excellent option at $20
  [OK] cheapest of two excellents:           expected=b, got=b — cheapest among excellent options at $20
  [OK] tie on cond+price picks first:        expected=a, got=a — tied on condition (excellent) and price ($20); top search match
  [OK] all same tier, cheapest wins:         expected=b, got=b — cheapest among good options at $15
  [OK] all fair, pick cheapest:              expected=b, got=b — cheapest among fair options at $10
  [OK] excellent beats cheaper good:         expected=b, got=b — only excellent option at $50
  [OK] 3 goods, middle price:                expected=b, got=b — cheapest among good options at $20
  [OK] excellent at same price as good:      expected=b, got=b — only excellent option at $20
  [OK] two excellent, one much cheaper:      expected=b, got=b — cheapest among excellent options at $10
  [OK] mixed; cheapest-excellent at pos 3:   expected=c, got=c — only excellent option at $18
```

**C2 — `serve.py::ask` → `agent.py::run_agent` branch, re-scored across mixed hit counts**
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

**C3 — `tools.py::compare_listings` row shape, per session**
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

**C4 — `serve.py::ask` on five bad payloads**
```
  payload='{}'                                     → HTTP 400  log_matched_400=True
  payload='{"query": ""}'                          → HTTP 400  log_matched_400=True
  payload='{"query": "   "}'                       → HTTP 400  log_matched_400=True
  payload='{"wardrobe": {"items": []}}'            → HTTP 400  log_matched_400=True
  payload='{"query": null}'                        → HTTP 400  log_matched_400=True
  log records added: 5, of which status=bad_request: 5
```

**C5 — `serve.py::_write_log` over 20 consecutive /ask requests**
```
  requests sent: 20
  log records added: 20
  valid JSON with required keys: 20
```

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
