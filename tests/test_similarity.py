
from datetime import datetime

from src.models.bug import Bug
from src.services.similarity import BugSimilarityEngine


def create_bug(
    bug_id: str,
    title: str,
    description: str,
    component: str = "checkout-service",
) -> Bug:
    return Bug(
        bug_id=bug_id,
        title=title,
        description=description,
        status="resolved",
        severity="high",
        component=component,
        created_at=datetime(2026, 1, 10),
        affected_version="1.4.0",
    )


def test_similarity_engine_returns_similar_bugs():
    target = create_bug(
        "BUG-001",
        "Checkout timeout with coupon",
        "Checkout times out when coupon validation runs.",
    )

    related = create_bug(
        "BUG-002",
        "Checkout hangs during coupon validation",
        "The checkout process hangs when validating a coupon.",
    )

    unrelated = create_bug(
        "BUG-003",
        "Search results are missing products",
        "The product search index fails to return some products.",
        component="search-service",
    )

    engine = BugSimilarityEngine(
        use_git_evidence=False,
        use_adjusted_weights=False,
    )

    results = engine.find_similar(
        target_bug=target,
        bugs=[target, related, unrelated],
        top_k=2,
    )

    result_ids = [result.bug_id for result in results]

    assert len(results) == 2
    assert "BUG-002" in result_ids
    assert all(0.0 <= result.score <= 1.0 for result in results)


def test_similarity_engine_excludes_target_bug():
    target = create_bug(
        "BUG-001",
        "Checkout timeout with coupon",
        "Checkout times out when coupon validation runs.",
    )

    related = create_bug(
        "BUG-002",
        "Checkout hangs during coupon validation",
        "The checkout process hangs when validating a coupon.",
    )

    engine = BugSimilarityEngine(
        use_git_evidence=False,
        use_adjusted_weights=False,
    )

    results = engine.find_similar(
        target_bug=target,
        bugs=[target, related],
        top_k=5,
    )

    result_ids = [result.bug_id for result in results]

    assert "BUG-001" not in result_ids
    assert "BUG-002" in result_ids
    assert len(results) == 1
