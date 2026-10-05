from src.models.bug import Bug
from src.models.commit import Commit
from src.services.commit_service import CommitService


class BugCommitService:
    """
    Connects bug reports with their related Git commits.
    """

    def __init__(
        self,
        bugs: list[Bug],
        commits: list[Commit],
    ):
        self.bugs = bugs
        self.commits = commits

        self.commit_service = CommitService(commits)

    def get_commit_for_bug(
        self,
        bug: Bug,
    ) -> Commit | None:
        """
        Returns the Git commit linked to a bug.
        """

        if not bug.linked_commit:
            return None

        return self.commit_service.get_commit(
            bug.linked_commit
        )

    def get_bugs_for_commit(
        self,
        commit: Commit,
    ) -> list[Bug]:
        """
        Returns all bugs linked to a commit.
        """

        bug_ids = set(commit.bug_ids)

        return [
            bug
            for bug in self.bugs
            if bug.bug_id in bug_ids
        ]

    def get_related_bugs(
        self,
        bug: Bug,
    ) -> list[Bug]:
        """
        Finds bugs whose linked commits changed at least
        one of the same files as the target bug's commit.
        """

        target_commit = self.get_commit_for_bug(bug)

        if target_commit is None:
            return []

        related_commits = (
            self.commit_service.get_related_commits(
                target_commit
            )
        )

        related_bug_ids = {
            bug_id
            for commit in related_commits
            for bug_id in commit.bug_ids
        }

        return [
            candidate
            for candidate in self.bugs
            if candidate.bug_id in related_bug_ids
        ]