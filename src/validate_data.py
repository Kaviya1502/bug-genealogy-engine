import json
from pathlib import Path

from src.models.bug import Bug


DATA_PATH = Path("data/synthetic/bugs.json")


def load_bugs() -> list[Bug]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        raw_bugs = json.load(file)

    return [Bug.model_validate(bug) for bug in raw_bugs]


if __name__ == "__main__":
    bugs = load_bugs()

    print(f"Loaded {len(bugs)} bugs successfully.")

    for bug in bugs:
        print(f"{bug.bug_id}: {bug.title}")