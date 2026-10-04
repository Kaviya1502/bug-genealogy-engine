from datetime import datetime


def temporal_similarity(
    date_a: datetime,
    date_b: datetime,
    max_days: int = 30,
) -> float:
    """
    Returns a temporal similarity score based on the distance
    between two dates.

    1.0 -> same date
    0.0 -> max_days apart or more

    The score decreases linearly as the time difference increases.
    """

    difference_days = abs(
        (date_a - date_b).total_seconds()
    ) / 86400

    if difference_days >= max_days:
        return 0.0

    return round(
        1.0 - (difference_days / max_days),
        4,
    )