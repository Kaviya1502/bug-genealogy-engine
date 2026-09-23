import json
from datetime import datetime
from pathlib import Path

from src.models.bug import Bug


BUGS_PATH = Path("data/synthetic/bugs.json")
FAMILIES_PATH = Path("data/synthetic/bug_families.json")


def test_bug_creation():
    bug = Bug(
        bug_id="BUG-001",
        title="Payment timeout",
        description="Payment requests timeout after 30 seconds.",
        status="resolved",
        severity="high",
        component="payment-service",
        created_at=datetime(2026, 1, 10, 10, 30),
        resolved_at=datetime(2026, 1, 12, 15, 0),
        affected_version="1.4.0",
        fixed_version="1.4.1",
        linked_commit="COMMIT-014",
        linked_test="TEST-021",
        root_cause="Payment gateway timeout configuration",
    )

    assert bug.bug_id == "BUG-001"
    assert bug.severity == "high"
    assert bug.component == "payment-service"


def load_bugs():
    with BUGS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_families():
    with FAMILIES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_synthetic_dataset():
    raw_bugs = load_bugs()

    bugs = [Bug.model_validate(bug) for bug in raw_bugs]

    assert len(bugs) == 10
    assert all(isinstance(bug, Bug) for bug in bugs)


def test_bug_families():
    bugs = load_bugs()
    families = load_families()

    bug_ids = {bug["bug_id"] for bug in bugs}

    family_bug_ids = [
        bug_id
        for family in families.values()
        for bug_id in family["bugs"]
    ]

    assert len(family_bug_ids) == len(set(family_bug_ids))
    assert set(family_bug_ids) == bug_ids

