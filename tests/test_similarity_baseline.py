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


def test_similarity_baseline():
    bugs = load_bugs()
    families = load_families()

    bug_to_family = build_bug_to_family_map(families)

    engine = BugSimilarityEngine()

    precisions = []

    for target_bug in bugs:
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

        precisions.append(precision)

        print(f"\n{'=' * 70}")
        print(
            f"{target_bug.bug_id}: {target_bug.title}"
        )
        print(f"Family: {target_family}")
        print("Top-3 similar bugs:")

        for rank, result in enumerate(results, start=1):
            result_family = bug_to_family[result.bug_id]

            match = "YES" if result_family == target_family else "NO"

            print(
                f"  {rank}. {result.bug_id} | "
                f"{result.score:.4f} | "
                f"{result.title}"
            )
            print(
                f"     Family: {result_family} | "
                f"Same family: {match}"
            )

        print(f"Precision: {precision:.2%}")

    average_precision = sum(precisions) / len(precisions)

    print(f"\n{'=' * 70}")
    print(
        f"Average Top-3 family precision: "
        f"{average_precision:.2%}"
    )

    assert len(precisions) == len(bugs)