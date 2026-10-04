from datetime import datetime

from src.models.bug import Bug
from src.services.similarity import BugSimilarityEngine


def create_bug(
    bug_id: str,
    title: str,
    description: str,
    component: str,
    version: str,
    created_at: datetime,
) -> Bug:
    return Bug(
        bug_id=bug_id,
        title=title,
        description=description,
        status="resolved",
        severity="high",
        component=component,
        created_at=created_at,
        affected_version=version,
    )


def test_similarity_engine_returns_similar_bugs():
    bugs = [
        create_bug(
            bug_id="BUG-001",
            title="Checkout timeout with coupon",
            description="Checkout times out when a coupon is applied.",
            component="checkout-service",
            version="1.4.0",
            created_at=datetime(2026, 1, 10),
        ),
        create_bug(
            bug_id="BUG-002",
            title="Checkout hangs on promotion",
            description="Checkout becomes slow when promotional codes are used.",
            component="checkout-service",
            version="1.4.1",
            created_at=datetime(2026, 1, 12),
        ),
        create_bug(
            bug_id="BUG-003",
            title="Search returns empty results",
            description="Product search sometimes returns no results.",
            component="search-service",
            version="1.4.3",
            created_at=datetime(2026, 3, 10),
        ),
    ]

    engine = BugSimilarityEngine()

    results = engine.find_similar(
        target_bug=bugs[0],
        bugs=bugs,
        top_k=2,
    )

    assert len(results) == 2

    assert all(result.bug_id != "BUG-001" for result in results)

    assert results[0].bug_id == "BUG-002"

    assert 0.0 <= results[0].component_score <= 1.0
    assert 0.0 <= results[0].temporal_score <= 1.0
    assert 0.0 <= results[0].version_score <= 1.0
    assert 0.0 <= results[0].score <= 1.0


def test_similarity_engine_excludes_target_bug():
    bug = create_bug(
        bug_id="BUG-001",
        title="Checkout timeout",
        description="Checkout request times out.",
        component="checkout-service",
        version="1.4.0",
        created_at=datetime(2026, 1, 10),
    )

    engine = BugSimilarityEngine()

    results = engine.find_similar(
        target_bug=bug,
        bugs=[bug],
        top_k=5,
    )

    assert results == []