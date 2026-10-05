from datetime import datetime

from src.models.bug import Bug
from src.models.commit import Commit
from src.services.bug_file_relationship import (
    BugFileRelationshipService,
)


def create_bug(
    bug_id: str,
    linked_commit: str | None,
) -> Bug:
    return Bug(
        bug_id=bug_id,
        title=f"Bug {bug_id}",
        description=f"Description for {bug_id}",
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
        message=f"Commit {commit_id}",
        author="test-user",
        timestamp=datetime(2026, 1, 10),
        version="1.4.1",
        files_changed=files_changed,
        bug_ids=bug_ids,
    )


def test_get_file_overlap():
    bugs = [
        create_bug("BUG-001", "COMMIT-101"),
        create_bug("BUG-004", "COMMIT-115"),
    ]

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
    ]

    service = BugFileRelationshipService(
        bugs,
        commits,
    )

    score = service.get_file_overlap(
        bugs[0],
        bugs[1],
    )

    assert score == 0.5


def test_no_file_overlap():
    bugs = [
        create_bug("BUG-001", "COMMIT-101"),
        create_bug("BUG-002", "COMMIT-104"),
    ]

    commits = [
        create_commit(
            "COMMIT-101",
            [
                "checkout/coupon_validator.py",
            ],
            ["BUG-001"],
        ),
        create_commit(
            "COMMIT-104",
            [
                "search/indexer.py",
            ],
            ["BUG-002"],
        ),
    ]

    service = BugFileRelationshipService(
        bugs,
        commits,
    )

    score = service.get_file_overlap(
        bugs[0],
        bugs[1],
    )

    assert score == 0.0


def test_unlinked_bug_has_no_file_overlap():
    bugs = [
        create_bug("BUG-001", None),
        create_bug("BUG-002", "COMMIT-104"),
    ]

    commits = [
        create_commit(
            "COMMIT-104",
            [
                "search/indexer.py",
            ],
            ["BUG-002"],
        ),
    ]

    service = BugFileRelationshipService(
        bugs,
        commits,
    )

    score = service.get_file_overlap(
        bugs[0],
        bugs[1],
    )

    assert score == 0.0