
from datetime import datetime

from src.models.bug import Bug
from src.models.commit import Commit
from src.services.similarity import BugSimilarityEngine


def create_bug(
    bug_id: str,
    title: str,
    description: str,
    linked_commit: str,
) -> Bug:
    return Bug(
        bug_id=bug_id,
        title=title,
        description=description,
        status="resolved",
        severity="high",
        component="checkout-service",
        created_at=datetime(2026, 1, 10),
        affected_version="1.4.0",
        linked_commit=linked_commit,
    )


def create_commit(
    commit_id: str,
    files_changed: list[str],
    bug_ids: list[str],
) -> Commit:
    return Commit(
        commit_id=commit_id,
        message=f"Fix for {bug_ids[0]}",
        author="test-user",
        timestamp=datetime(2026, 1, 10),
        version="1.4.1",
        files_changed=files_changed,
        bug_ids=bug_ids,
    )


def test_git_file_overlap_is_included_in_similarity_results():
    target = create_bug(
        "BUG-001",
        "Checkout timeout with coupon",
        "Checkout times out when coupon validation runs.",
        "COMMIT-101",
    )

    related = create_bug(
        "BUG-004",
        "Checkout hangs on promotional code",
        "Checkout hangs when promotional codes are applied.",
        "COMMIT-115",
    )

    unrelated = create_bug(
        "BUG-009",
        "Checkout fails for discount codes",
        "A discount rule parser rejects certain coupon formats.",
        "COMMIT-142",
    )

    commits = [
        create_commit(
            "COMMIT-101",
            [
                "checkout/coupon_validator.py",
                "checkout/service.py",
            ],
            ["BUG-001"],
        ),
        create_commit(
            "COMMIT-115",
            [
                "checkout/coupon_validator.py",
            ],
            ["BUG-004"],
        ),
        create_commit(
            "COMMIT-142",
            [
                "checkout/discount_rule_parser.py",
            ],
            ["BUG-009"],
        ),
    ]

    engine = BugSimilarityEngine(
        commits=commits,
        use_git_evidence=True,
        use_adjusted_weights=True,
    )

    results = engine.find_similar(
        target_bug=target,
        bugs=[target, related, unrelated],
        top_k=2,
    )

    results_by_id = {
        result.bug_id: result
        for result in results
    }

    assert results_by_id["BUG-004"].file_overlap_score == 0.5
    assert results_by_id["BUG-009"].file_overlap_score == 0.0

    # Compare with the same adjusted weights but without Git evidence.
    engine_without_git = BugSimilarityEngine(
        commits=commits,
        use_git_evidence=False,
        use_adjusted_weights=True,
    )

    results_without_git = engine_without_git.find_similar(
        target_bug=target,
        bugs=[target, related, unrelated],
        top_k=2,
    )

    scores_without_git = {
        result.bug_id: result.score
        for result in results_without_git
    }

    # Shared files must contribute the configured 10% overlap bonus.
    assert results_by_id["BUG-004"].score == round(
        scores_without_git["BUG-004"] + 0.5 * 0.10,
        4,
    )
