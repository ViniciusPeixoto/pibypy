import pytest

from utils.big_math import (
    _fits,
    _calculate_division,
    division,
    DECIMAL_LIMIT,
)

@pytest.mark.parametrize(
        "numerator, denominator, expected",
        [("3", "2", True), ("2", "3", False),]
)
def test_fits(numerator, denominator, expected):
    result = _fits(numerator, denominator)

    assert result == expected


@pytest.mark.parametrize(
        "numerator, denominator, expected",
        [
            ("3", "2", ("1", "1")),
            ("2", "3", ("0", "2")),
            ("4", "4", ("1", "0")),
            ("4", "2", ("2", "0")),
        ]
)
def test_calculate_division(numerator, denominator, expected):
    result = _calculate_division(numerator, denominator)

    assert result == expected


@pytest.mark.parametrize(
        "numerator, denominator, fixed, repeating_decimal",
        [
            ("3", "2", "1.5", ""),
            ("1", "3", "0.", "3"),
            ("1", "7", "0.", "142857"),
        ],
        indirect=["repeating_decimal"]
)
def test_division(numerator, denominator, fixed, repeating_decimal):
    result = division(numerator, denominator)

    assert result == fixed + repeating_decimal
