def component_similarity(
    component_a: str,
    component_b: str,
) -> float:
    """
    Returns a structured similarity score based on component.

    1.0 -> same component
    0.0 -> different components
    """

    return 1.0 if component_a == component_b else 0.0


def combined_similarity(
    semantic_score: float,
    component_score: float,
    temporal_score: float = 0.0,
    version_score: float = 0.0,
    semantic_weight: float = 0.6,
    component_weight: float = 0.2,
    temporal_weight: float = 0.1,
    version_weight: float = 0.1,
) -> float:
    """
    Combines multiple evidence signals.

    Default weighting:
    - Semantic: 60%
    - Component: 20%
    - Temporal: 10%
    - Version: 10%
    """

    combined_score = (
        semantic_score * semantic_weight
        + component_score * component_weight
        + temporal_score * temporal_weight
        + version_score * version_weight
    )

    return round(combined_score, 4)