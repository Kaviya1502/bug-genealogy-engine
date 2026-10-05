from src.models.commit import Commit


class CommitService:
    """
    Provides lookup and relationship operations for Git commits.
    """

    def __init__(self, commits: list[Commit]):
        self.commits = commits

        self._commit_index = {
            commit.commit_id: commit
            for commit in commits
        }

    def get_commit(self, commit_id: str) -> Commit | None:
        """
        Returns a commit by its ID.

        Returns None if the commit does not exist.
        """

        return self._commit_index.get(commit_id)

    def get_commits_for_file(
        self,
        file_path: str,
    ) -> list[Commit]:
        """
        Returns all commits that changed a given file.
        """

        return [
            commit
            for commit in self.commits
            if file_path in commit.files_changed
        ]

    def get_related_commits(
        self,
        commit: Commit,
    ) -> list[Commit]:
        """
        Returns other commits that changed at least one
        file in common with the supplied commit.
        """

        related = []

        commit_files = set(commit.files_changed)

        for candidate in self.commits:
            if candidate.commit_id == commit.commit_id:
                continue

            candidate_files = set(candidate.files_changed)

            if commit_files & candidate_files:
                related.append(candidate)

        return related