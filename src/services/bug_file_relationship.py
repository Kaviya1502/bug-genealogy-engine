from src.models.bug import Bug
from src.models.commit import Commit
from src.services.bug_commit_service import BugCommitService
from src.services.file_overlap import file_overlap_score


class BugFileRelationshipService:
    """
    Calculates file-level relationships between bugs.

    A bug is represented by the files changed in its linked commit.
    Bugs with overlapping files receive a higher relationship score.
    """

    def __init__(
        self,
        bugs: list[Bug],
        commits: list[Commit],
    ):
        self.bugs = bugs
        self.commits = commits

        self.bug_commit_service = BugCommitService(
            bugs,
            commits,
        )

    def get_file_overlap(
        self,
        bug_a: Bug,
        bug_b: Bug,
    ) -> float:
        """
        Returns the file overlap score between two bugs.

        1.0 -> both bugs changed exactly the same files
        0.0 -> no files in common
        """

        commit_a = self.bug_commit_service.get_commit_for_bug(
            bug_a
        )

        commit_b = self.bug_commit_service.get_commit_for_bug(
            bug_b
        )

        if commit_a is None or commit_b is None:
            return 0.0

        return file_overlap_score(
            commit_a.files_changed,
            commit_b.files_changed,
        )