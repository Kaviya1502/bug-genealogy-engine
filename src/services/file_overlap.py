def file_overlap_score(
    files_a: list[str],
    files_b: list[str],
) -> float:
    """
    Calculates the Jaccard similarity between two sets of files.

    1.0 -> exactly the same files
    0.0 -> no files in common
    """

    set_a = set(files_a)
    set_b = set(files_b)

    if not set_a or not set_b:
        return 0.0

    intersection = set_a & set_b
    union = set_a | set_b

    return round(
        len(intersection) / len(union),
        4,
    )