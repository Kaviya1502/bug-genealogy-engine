from datetime import datetime

from src.models.bug import Bug
from src.models.commit import Commit
from src.services.bug_commit_service import BugCommitService


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


def test_get_commit_for_bug():
    bugs = [
        create_bug(
            "BUG-001",
            "COMMIT-101",
        ),
    ]

    commits = [
        create_commit(
            "COMMIT-101",
            ["checkout/coupon_validator.py"],
            ["BUG-001"],
        ),
    ]

    service = BugCommitService(
        bugs,
        commits,
    )

    commit = service.get_commit_for_bug(bugs[0])

    assert commit is not None
    assert commit.commit_id == "COMMIT-101"


def test_get_commit_for_unlinked_bug():
    bugs = [
        create_bug(
            "BUG-001",
            None,
        ),
    ]

    service = BugCommitService(
        bugs,
        [],
    )

    commit = service.get_commit_for_bug(bugs[0])

    assert commit is None


def test_get_bugs_for_commit():
    bugs = [
        create_bug(
            "BUG-001",
            "COMMIT-101",
        ),
        create_bug(
            "BUG-002",
            "COMMIT-101",
        ),
    ]

    commits = [
        create_commit(
            "COMMIT-101",
            ["checkout/service.py"],
            ["BUG-001", "BUG-002"],
        ),
    ]

    service = BugCommitService(
        bugs,
        commits,
    )

    results = service.get_bugs_for_commit(
        commits[0]
    )

    result_ids = {
        bug.bug_id
        for bug in results
    }

    assert result_ids == {
        "BUG-001",
        "BUG-002",
    }


def test_get_related_bugs():
    bugs = [
        create_bug(
            "BUG-001",
            "COMMIT-101",
        ),
        create_bug(
            "BUG-004",
            "COMMIT-115",
        ),
        create_bug(
            "BUG-007",
            "COMMIT-131",
        ),
        create_bug(
            "BUG-002",
            "COMMIT-104",
        ),
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
        create_commit(
            "COMMIT-131",
            [
                "checkout/coupon_validator.py",
                "checkout/discount_service.py",
            ],
            ["BUG-007"],
        ),
        create_commit(
            "COMMIT-104",
            [
                "search/indexer.py",
            ],
            ["BUG-002"],
        ),
    ]

    service = BugCommitService(
        bugs,
        commits,
    )

    results = service.get_related_bugs(
        bugs[0]
    )

    result_ids = {
        bug.bug_id
        for bug in results
    }

    assert result_ids == {
        "BUG-004",
        "BUG-007",
    }