import json
from pathlib import Path

from src.models.bug import Bug
from src.services.similarity import BugSimilarityEngine


DATA_PATH = Path("data/synthetic/bugs.json")


def load_bugs() -> list[Bug]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        raw_bugs = json.load(file)

    return [Bug.model_validate(bug) for bug in raw_bugs]


if __name__ == "__main__":
    bugs = load_bugs()

    target_bug = bugs[0]

    engine = BugSimilarityEngine()

    results = engine.find_similar(
        target_bug=target_bug,
        bugs=bugs,
        top_k=5,
    )

    print(f"\nTarget bug: {target_bug.bug_id}")
    print(f"Title: {target_bug.title}\n")

    print("Similar bugs:")

    for rank, result in enumerate(results, start=1):
        print(
            f"{rank}. {result.bug_id} | "
            f"Final: {result.score:.4f} | "
            f"Component: {result.component_score:.4f} | "
            f"Temporal: {result.temporal_score:.4f} | "
            f"Version: {result.version_score:.4f} | "
            f"{result.title}"
        )