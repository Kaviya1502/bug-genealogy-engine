from datetime import datetime

from src.models.bug import Bug


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