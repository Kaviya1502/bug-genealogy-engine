from datetime import datetime

from pydantic import BaseModel


class Commit(BaseModel):
    commit_id: str
    message: str
    author: str
    timestamp: datetime
    version: str
    files_changed: list[str]
    bug_ids: list[str] = []