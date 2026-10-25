
import json
from pathlib import Path

from src.models.bug import Bug
from src.models.commit import Commit
from src.services.similarity import BugSimilarityEngine


BUGS_PATH = Path("data/synthetic/bugs.json")
FAMILIES_PATH = Path("data/synthetic/bug_families.json")
COMMITS_PATH = Path("data/synthetic/commits.json")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_bugs() -> list[Bug]:
    return [
        Bug.model_validate(item)
        for item in load_json(BUGS_PATH)
    ]


def load_commits() -> list[Commit]:
    return [
        Commit.model_validate(item)
        for item in load_json(COMMITS_PATH)
    ]


def build_bug_to_family_map(families: dict) -> dict[str, str]:
    return {
        bug_id: family_id
        for family_id, family in families.items()
        for bug_id in family["bugs"]
    }


def evaluate_engine(
    engine: BugSimilarityEngine,
    bugs: list[Bug],
    bug_to_family: dict[str, str],
    top_k: int = 3,
) -> tuple[float, dict[str, float]]:
    precisions = {}

    for target_bug in bugs:
        results = engine.find_similar(
            target_bug=target_bug,
            bugs=bugs,
            top_k=top_k,
        )

        target_family = bug_to_family[target_bug.bug_id]

        correct_matches = sum(
            bug_to_family[result.bug_id] == target_family
            for result in results
        )

        precision = (
            correct_matches / len(results)
            if results
            else 0.0
        )

        precisions[target_bug.bug_id] = precision

    average_precision = (
        sum(precisions.values()) / len(precisions)
        if precisions
        else 0.0
    )

    return average_precision, precisions


def test_compare_three_similarity_configurations():
    bugs = load_bugs()
    commits = load_commits()
    families = load_json(FAMILIES_PATH)
    bug_to_family = build_bug_to_family_map(families)

    # Configuration 1: Original scoring weights, without Git evidence.
    baseline_engine = BugSimilarityEngine(
        use_git_evidence=False,
        use_adjusted_weights=False,
    )

    # Configuration 2: Adjusted weights, without Git evidence.
    adjusted_engine = BugSimilarityEngine(
        commits=commits,
        use_git_evidence=False,
        use_adjusted_weights=True,
    )

    # Configuration 3: Adjusted weights, with Git file evidence.
    git_aware_engine = BugSimilarityEngine(
        commits=commits,
        use_git_evidence=True,
        use_adjusted_weights=True,
    )

    baseline_average, baseline_per_bug = evaluate_engine(
        baseline_engine,
        bugs,
        bug_to_family,
    )

    adjusted_average, adjusted_per_bug = evaluate_engine(
        adjusted_engine,
        bugs,
        bug_to_family,
    )

    git_average, git_per_bug = evaluate_engine(
        git_aware_engine,
        bugs,
        bug_to_family,
    )

    print("\n" + "=" * 88)
    print("BUG-FAMILY SIMILARITY: THREE-WAY EVALUATION")
    print("=" * 88)
    print(f"Number of bugs: {len(bugs)}")
    print("Metric: Average Top-3 family precision")
    print()
    print(
        f"{'Bug ID':<12}"
        f"{'Baseline':>14}"
        f"{'Adjusted':>14}"
        f"{'Git-aware':>14}"
    )
    print("-" * 54)

    for bug in bugs:
        bug_id = bug.bug_id

        print(
            f"{bug_id:<12}"
            f"{baseline_per_bug[bug_id]:>13.2%}"
            f"{adjusted_per_bug[bug_id]:>14.2%}"
            f"{git_per_bug[bug_id]:>14.2%}"
        )

    print("-" * 54)
    print(
        f"{'AVERAGE':<12}"
        f"{baseline_average:>13.2%}"
        f"{adjusted_average:>14.2%}"
        f"{git_average:>14.2%}"
    )

    print("\nChanges in average Top-3 family precision:")
    print(
        "Adjusted weights vs baseline: "
        f"{(adjusted_average - baseline_average) * 100:+.2f} "
        "percentage points"
    )
    print(
        "Git evidence vs adjusted weights: "
        f"{(git_average - adjusted_average) * 100:+.2f} "
        "percentage points"
    )
    print(
        "Git-aware vs baseline: "
        f"{(git_average - baseline_average) * 100:+.2f} "
        "percentage points"
    )

    assert len(baseline_per_bug) == len(bugs)
    assert len(adjusted_per_bug) == len(bugs)
    assert len(git_per_bug) == len(bugs)

    for scores in (
        baseline_per_bug,
        adjusted_per_bug,
        git_per_bug,
    ):
        assert all(0.0 <= value <= 1.0 for value in scores.values())

    assert 0.0 <= baseline_average <= 1.0
    assert 0.0 <= adjusted_average <= 1.0
    assert 0.0 <= git_average <= 1.0
