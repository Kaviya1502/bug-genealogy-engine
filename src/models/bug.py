from datetime import datetime

from pydantic import BaseModel


class Bug(BaseModel):
    bug_id: str
    title: str
    description: str
    status: str
    severity: str
    component: str
    created_at: datetime
    resolved_at: datetime | None = None
    affected_version: str
    fixed_version: str | None = None
    linked_commit: str | None = None
    linked_test: str | None = None
    root_cause: str | None = None