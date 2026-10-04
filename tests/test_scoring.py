from src.services.scoring import (
    combined_similarity,
    component_similarity,
)


def test_same_component():
    score = component_similarity(
        "checkout-service",
        "checkout-service",
    )

    assert score == 1.0


def test_different_component():
    score = component_similarity(
        "checkout-service",
        "payment-service",
    )

    assert score == 0.0


def test_combined_similarity():
    score = combined_similarity(
        semantic_score=0.8,
        component_score=1.0,
        temporal_score=0.5,
        version_score=0.6,
    )

    expected = (
        0.8 * 0.6
        + 1.0 * 0.2
        + 0.5 * 0.1
        + 0.6 * 0.1
    )

    assert score == round(expected, 4)


def test_combined_similarity_different_component():
    score = combined_similarity(
        semantic_score=0.8,
        component_score=0.0,
        temporal_score=0.5,
        version_score=0.6,
    )

    expected = (
        0.8 * 0.6
        + 0.0 * 0.2
        + 0.5 * 0.1
        + 0.6 * 0.1
    )

    assert score == round(expected, 4)


def test_combined_similarity_same_version():
    score = combined_similarity(
        semantic_score=0.8,
        component_score=1.0,
        temporal_score=1.0,
        version_score=1.0,
    )

    expected = (
        0.8 * 0.6
        + 1.0 * 0.2
        + 1.0 * 0.1
        + 1.0 * 0.1
    )

    assert score == round(expected, 4)