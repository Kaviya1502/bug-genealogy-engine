import json
from pathlib import Path

from src.models.commit import Commit


DATA_PATH = Path("data/synthetic/commits.json")


def load_commits() -> list[Commit]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        raw_commits = json.load(file)

    return [
        Commit.model_validate(commit)
        for commit in raw_commits
    ]


if __name__ == "__main__":
    commits = load_commits()

    print(f"Loaded {len(commits)} commits successfully.")

    for commit in commits:
        print(
            f"{commit.commit_id}: "
            f"{commit.message} | "
            f"Files: {len(commit.files_changed)}"
        )