from dataclasses import dataclass

from sentence_transformers import SentenceTransformer

from src.models.bug import Bug
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
    component_score: float
    temporal_score: float
    version_score: float


class BugSimilarityEngine:
    """
    Finds related bugs using multiple evidence signals.

    Signals currently used:
    - semantic similarity
    - component similarity
    - temporal similarity
    - version similarity

    The engine intentionally does not use:
    - root_cause
    - bug family labels

    This prevents data leakage during similarity detection.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

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

        if not candidate_bugs:
            return []

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

        for semantic_score, index in zip(
            semantic_scores,
            indices,
        ):
            bug = candidate_bugs[index]

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

            final_score = combined_similarity(
                semantic_score=float(semantic_score),
                component_score=component_score,
                temporal_score=temporal_score,
                version_score=version_score,
            )

            results.append(
                SimilarBug(
                    bug_id=bug.bug_id,
                    title=bug.title,
                    score=final_score,
                    component_score=component_score,
                    temporal_score=temporal_score,
                    version_score=version_score,
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results[:top_k]