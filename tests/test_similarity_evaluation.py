import json
from pathlib import Path

from src.models.bug import Bug
from src.services.similarity import BugSimilarityEngine


BUGS_PATH = Path("data/synthetic/bugs.json")
FAMILIES_PATH = Path("data/synthetic/bug_families.json")


def load_bugs() -> list[Bug]:
    with BUGS_PATH.open("r", encoding="utf-8") as file:
        raw_bugs = json.load(file)

    return [Bug.model_validate(bug) for bug in raw_bugs]


def load_families() -> dict:
    with FAMILIES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_bug_to_family_map(families: dict) -> dict[str, str]:
    bug_to_family = {}

    for family_id, family in families.items():
        for bug_id in family["bugs"]:
            bug_to_family[bug_id] = family_id

    return bug_to_family


def test_top_3_similarity_family_precision():
    bugs = load_bugs()
    families = load_families()

    bug_to_family = build_bug_to_family_map(families)

    engine = BugSimilarityEngine()

    target_bug = next(
        bug for bug in bugs
        if bug.bug_id == "BUG-001"
    )

    results = engine.find_similar(
        target_bug=target_bug,
        bugs=bugs,
        top_k=3,
    )

    target_family = bug_to_family[target_bug.bug_id]

    correct_matches = sum(
        bug_to_family[result.bug_id] == target_family
        for result in results
    )

    precision = correct_matches / len(results)

    print(f"\nTarget bug: {target_bug.bug_id}")
    print(f"Target family: {target_family}")

    for result in results:
        print(
            f"{result.bug_id} -> "
            f"{bug_to_family[result.bug_id]} "
            f"({result.score:.4f})"
        )

    print(f"\nTop-3 family precision: {precision:.2%}")

    assert len(results) == 3
    assert precision >= 0