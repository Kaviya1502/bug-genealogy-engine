from datetime import datetime

from src.services.temporal import temporal_similarity


def test_same_date():
    score = temporal_similarity(
        datetime(2026, 1, 10),
        datetime(2026, 1, 10),
    )

    assert score == 1.0


def test_close_dates():
    score = temporal_similarity(
        datetime(2026, 1, 10),
        datetime(2026, 1, 20),
    )

    assert score == 0.6667


def test_maximum_distance():
    score = temporal_similarity(
        datetime(2026, 1, 10),
        datetime(2026, 2, 9),
    )

    assert score == 0.0


def test_beyond_maximum_distance():
    score = temporal_similarity(
        datetime(2026, 1, 10),
        datetime(2026, 3, 10),
    )

    assert score == 0.0