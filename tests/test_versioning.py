import pytest

from src.services.versioning import (
    parse_version,
    version_distance,
    version_similarity,
)


def test_parse_version():
    version = parse_version("1.4.3")

    assert version == (1, 4, 3)


def test_version_distance_patch_change():
    distance = version_distance(
        "1.4.1",
        "1.4.3",
    )

    assert distance == 2


def test_version_distance_minor_change():
    distance = version_distance(
        "1.4.0",
        "1.5.0",
    )

    assert distance == 10


def test_version_distance_major_change():
    distance = version_distance(
        "1.4.0",
        "2.4.0",
    )

    assert distance == 100


def test_version_distance_same_version():
    distance = version_distance(
        "1.4.3",
        "1.4.3",
    )

    assert distance == 0


def test_version_similarity_same_version():
    score = version_similarity(
        "1.4.3",
        "1.4.3",
    )

    assert score == 1.0


def test_version_similarity_close_patch_versions():
    score = version_similarity(
        "1.4.1",
        "1.4.3",
    )

    assert score == 0.8


def test_version_similarity_max_distance():
    score = version_similarity(
        "1.4.0",
        "1.5.0",
    )

    assert score == 0.0


def test_invalid_version():
    with pytest.raises(ValueError):
        parse_version("version-1.4")