
from dataclasses import dataclass

from sentence_transformers import SentenceTransformer

from src.models.bug import Bug
from src.models.commit import Commit
from src.services.bug_file_relationship import (
    BugFileRelationshipService,
)
from src.services.scoring import (
    combined_similarity,
    component_similarity,
)
from src.services.temporal import temporal_similarity
from src.services.vector_store import BugVectorStore
from src.services.versioning import version_similarity

MODEL_NAME = "all-MiniLM-L6-v2"


@dataclass
class SimilarBug:
    bug_id: str
    title: str
    score: float
    semantic_score: float
    component_score: float
    temporal_score: float
    version_score: float
    file_overlap_score: float


class BugSimilarityEngine:
    """
    Finds related bugs using semantic and engineering evidence.

    Scoring configurations:
    - original weights: 0.60, 0.20, 0.10, 0.10
    - adjusted weights: 0.55, 0.20, 0.10, 0.05
    - optional Git file-overlap contribution: 0.10

    Ground-truth family labels are not used as model inputs.
    """

    def __init__(
        self,
        model_name: str = MODEL_NAME,
        commits: list[Commit] | None = None,
        use_git_evidence: bool = False,
        use_adjusted_weights: bool = False,
    ):
        self.model = SentenceTransformer(model_name)
        self.commits = commits or []
        self.use_git_evidence = use_git_evidence
        self.use_adjusted_weights = use_adjusted_weights

        self.file_relationship_service = BugFileRelationshipService(
            bugs=[],
            commits=self.commits,
        )

    @staticmethod
    def _build_text(bug: Bug) -> str:
        return (
            f"Title: {bug.title}. "
            f"Description: {bug.description}. "
            f"Component: {bug.component}."
        )

    def create_embeddings(self, bugs: list[Bug]):
        texts = [self._build_text(bug) for bug in bugs]

        return self.model.encode(
            texts,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

    def find_similar(
        self,
        target_bug: Bug,
        bugs: list[Bug],
        top_k: int = 5,
    ) -> list[SimilarBug]:
        candidate_bugs = [
            bug for bug in bugs
            if bug.bug_id != target_bug.bug_id
        ]

        if not candidate_bugs or top_k <= 0:
            return []

        self.file_relationship_service.bugs = bugs
        self.file_relationship_service.bug_commit_service.bugs = bugs

        candidate_embeddings = self.create_embeddings(candidate_bugs)

        vector_store = BugVectorStore(
            dimension=candidate_embeddings.shape[1]
        )
        vector_store.add(candidate_embeddings)

        target_embedding = self.model.encode(
            self._build_text(target_bug),
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        semantic_scores, indices = vector_store.search(
            target_embedding,
            top_k=len(candidate_bugs),
        )

        results = []

        for semantic_score, index in zip(semantic_scores, indices):
            bug = candidate_bugs[int(index)]
            semantic_score = float(semantic_score)

            component_score = component_similarity(
                target_bug.component,
                bug.component,
            )
            temporal_score = temporal_similarity(
                target_bug.created_at,
                bug.created_at,
            )
            version_score = version_similarity(
                target_bug.affected_version,
                bug.affected_version,
            )

            file_score = 0.0
            if self.use_git_evidence and self.commits:
                file_score = (
                    self.file_relationship_service.get_file_overlap(
                        target_bug,
                        bug,
                    )
                )

            if self.use_adjusted_weights:
                semantic_weight = 0.55
                component_weight = 0.20
                temporal_weight = 0.10
                version_weight = 0.05
            else:
                semantic_weight = 0.60
                component_weight = 0.20
                temporal_weight = 0.10
                version_weight = 0.10

            final_score = combined_similarity(
                semantic_score=semantic_score,
                component_score=component_score,
                temporal_score=temporal_score,
                version_score=version_score,
                semantic_weight=semantic_weight,
                component_weight=component_weight,
                temporal_weight=temporal_weight,
                version_weight=version_weight,
            )

            if self.use_git_evidence and self.commits:
                final_score = round(
                    final_score + file_score * 0.10,
                    4,
                )

            results.append(
                SimilarBug(
                    bug_id=bug.bug_id,
                    title=bug.title,
                    score=final_score,
                    semantic_score=round(semantic_score, 4),
                    component_score=component_score,
                    temporal_score=temporal_score,
                    version_score=version_score,
                    file_overlap_score=file_score,
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results[:top_k]
