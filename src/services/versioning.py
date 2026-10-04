import re


def parse_version(version: str) -> tuple[int, ...]:
    """
    Converts a semantic-style version string into a tuple.

    Example:
        "1.4.3" -> (1, 4, 3)
    """

    match = re.fullmatch(
        r"(\d+)\.(\d+)\.(\d+)",
        version,
    )

    if not match:
        raise ValueError(
            f"Invalid version format: {version}"
        )

    return tuple(
        int(part)
        for part in match.groups()
    )


def version_distance(
    version_a: str,
    version_b: str,
) -> int:
    """
    Returns a weighted distance between two versions.

    Major version changes have the highest impact,
    followed by minor and patch changes.

    Weights:
        major = 100
        minor = 10
        patch = 1

    Example:
        1.4.0 -> 1.4.3 = 3
        1.4.0 -> 1.5.0 = 10
        1.4.0 -> 2.0.0 = 100
    """

    major_a, minor_a, patch_a = parse_version(version_a)
    major_b, minor_b, patch_b = parse_version(version_b)

    return (
        abs(major_a - major_b) * 100
        + abs(minor_a - minor_b) * 10
        + abs(patch_a - patch_b)
    )


def version_similarity(
    version_a: str,
    version_b: str,
    max_distance: int = 10,
) -> float:
    """
    Converts weighted version distance into a normalized
    similarity score.

    1.0 -> same version
    0.0 -> max_distance apart or more

    The score decreases linearly as the weighted distance increases.
    """

    distance = version_distance(
        version_a,
        version_b,
    )

    if distance >= max_distance:
        return 0.0

    return round(
        1.0 - (distance / max_distance),
        4,
    )