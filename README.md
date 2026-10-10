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
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



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

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



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

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
