"""
The runs your test needs. <- UNIT 4, MILESTONE 3

Each criterion has a scenario set here. run_eval.py runs every scenario five
separate times with caching disabled and writes the evidence under results/.
"""

SCENARIOS = [
    {
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        "name": "state and fit card for matching item",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        "name": "fit card includes item price",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    # Criterion 5 is measured over ten distinct queries with price ceilings.
    {"name": "budget filter: graphic tee", "query": "graphic tee under $30", "wardrobe": "example", "criterion": 5},
    {"name": "budget filter: denim jacket", "query": "denim jacket under $50", "wardrobe": "example", "criterion": 5},
    {"name": "budget filter: leather boots", "query": "leather boots under $60", "wardrobe": "example", "criterion": 5},
    {"name": "budget filter: wool sweater", "query": "wool sweater under $40", "wardrobe": "example", "criterion": 5},
    {"name": "budget filter: vintage jeans", "query": "vintage jeans under $35", "wardrobe": "example", "criterion": 5},
    {"name": "budget filter: canvas sneakers", "query": "canvas sneakers under $45", "wardrobe": "example", "criterion": 5},
    {"name": "budget filter: floral dress", "query": "floral dress under $50", "wardrobe": "example", "criterion": 5},
    {"name": "budget filter: corduroy pants", "query": "corduroy pants under $35", "wardrobe": "example", "criterion": 5},
    {"name": "budget filter: silk blouse", "query": "silk blouse under $40", "wardrobe": "example", "criterion": 5},
    {"name": "budget filter: crossbody bag", "query": "crossbody bag under $30", "wardrobe": "example", "criterion": 5},
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about malformed scenarios before a long run."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} - "
                f"it should be one of {WARDROBES}"
            )
    return problems
