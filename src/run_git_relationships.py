import json
from pathlib import Path

from src.models.bug import Bug
from src.models.commit import Commit
from src.services.bug_commit_service import BugCommitService


BUGS_PATH = Path("data/synthetic/bugs.json")
COMMITS_PATH = Path("data/synthetic/commits.json")


def load_bugs() -> list[Bug]:
    with BUGS_PATH.open("r", encoding="utf-8") as file:
        raw_bugs = json.load(file)

    return [
        Bug.model_validate(bug)
        for bug in raw_bugs
    ]


def load_commits() -> list[Commit]:
    with COMMITS_PATH.open("r", encoding="utf-8") as file:
        raw_commits = json.load(file)

    return [
        Commit.model_validate(commit)
        for commit in raw_commits
    ]


if __name__ == "__main__":
    bugs = load_bugs()
    commits = load_commits()

    service = BugCommitService(
        bugs,
        commits,
    )

    target_bug = bugs[0]

    commit = service.get_commit_for_bug(
        target_bug
    )

    related_bugs = service.get_related_bugs(
        target_bug
    )

    print(f"\nTarget bug: {target_bug.bug_id}")
    print(f"Title: {target_bug.title}")

    if commit:
        print(f"Linked commit: {commit.commit_id}")
        print("Files changed:")

        for file_path in commit.files_changed:
            print(f"  - {file_path}")

    print("\nRelated bugs through shared files:")

    for bug in related_bugs:
        print(
            f"  - {bug.bug_id}: "
            f"{bug.title}"
        )