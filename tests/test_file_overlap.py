from src.services.file_overlap import file_overlap_score


def test_exact_same_files():
    score = file_overlap_score(
        [
            "checkout/service.py",
            "checkout/coupon_validator.py",
        ],
        [
            "checkout/service.py",
            "checkout/coupon_validator.py",
        ],
    )

    assert score == 1.0


def test_partial_file_overlap():
    score = file_overlap_score(
        [
            "checkout/service.py",
            "checkout/coupon_validator.py",
        ],
        [
            "checkout/coupon_validator.py",
            "checkout/discount_service.py",
        ],
    )

    assert score == 0.3333


def test_no_file_overlap():
    score = file_overlap_score(
        [
            "checkout/service.py",
        ],
        [
            "search/indexer.py",
        ],
    )

    assert score == 0.0


def test_empty_file_lists():
    score = file_overlap_score(
        [],
        ["checkout/service.py"],
    )

    assert score == 0.0