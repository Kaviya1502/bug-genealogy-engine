from datetime import datetime

from src.models.commit import Commit
from src.services.commit_service import CommitService


def create_commit(
    commit_id: str,
    files_changed: list[str],
) -> Commit:
    return Commit(
        commit_id=commit_id,
        message=f"Commit {commit_id}",
        author="test-user",
        timestamp=datetime(2026, 1, 1),
        version="1.4.1",
        files_changed=files_changed,
        bug_ids=[],
    )


def test_get_commit():
    commits = [
        create_commit(
            "COMMIT-101",
            ["checkout/coupon_validator.py"],
        ),
        create_commit(
            "COMMIT-115",
            ["checkout/service.py"],
        ),
    ]

    service = CommitService(commits)

    commit = service.get_commit("COMMIT-101")

    assert commit is not None
    assert commit.commit_id == "COMMIT-101"


def test_get_missing_commit():
    service = CommitService([])

    commit = service.get_commit("COMMIT-999")

    assert commit is None


def test_get_commits_for_file():
    commits = [
        create_commit(
            "COMMIT-101",
            [
                "checkout/coupon_validator.py",
                "checkout/service.py",
            ],
        ),
        create_commit(
            "COMMIT-115",
            [
                "checkout/coupon_validator.py",
            ],
        ),
        create_commit(
            "COMMIT-104",
            [
                "search/indexer.py",
            ],
        ),
    ]

    service = CommitService(commits)

    results = service.get_commits_for_file(
        "checkout/coupon_validator.py"
    )

    result_ids = {
        commit.commit_id
        for commit in results
    }

    assert result_ids == {
        "COMMIT-101",
        "COMMIT-115",
    }


def test_get_related_commits():
    commits = [
        create_commit(
            "COMMIT-101",
            [
                "checkout/coupon_validator.py",
                "checkout/service.py",
            ],
        ),
        create_commit(
            "COMMIT-115",
            [
                "checkout/coupon_validator.py",
            ],
        ),
        create_commit(
            "COMMIT-131",
            [
                "checkout/discount_service.py",
            ],
        ),
        create_commit(
            "COMMIT-104",
            [
                "search/indexer.py",
            ],
        ),
    ]

    service = CommitService(commits)

    target = service.get_commit("COMMIT-101")

    assert target is not None

    results = service.get_related_commits(target)

    result_ids = {
        commit.commit_id
        for commit in results
    }

    assert result_ids == {
        "COMMIT-115",
    }