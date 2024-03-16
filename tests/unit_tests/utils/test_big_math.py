import pytest

from utils.big_math import (
    _fits,
    _calculate_division,
    division,
    _match_number_sizes,
    _add_string,
    add,
    _sub_string,
    sub,
    multiplication,
    Decimal,
)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({}, Decimal()),
        ({"number": ""}, Decimal(number="0.0")),
        ({"whole": ""}, Decimal(number="0.0")),
        ({"decimal": ""}, Decimal(number="0.0")),
        ({"is_negative": True}, Decimal(number="0.0", is_negative=False)),
        ({"number": "3.14"}, Decimal(whole="3", decimal="14", is_negative=False)),
        ({"number": "-3.14"}, Decimal(whole="3", decimal="14", is_negative=True)),
        ({"number": "314"}, Decimal(whole="314", decimal="0", is_negative=False)),
        ({"number": ".56"}, Decimal(whole="0", decimal="56", is_negative=False)),
    ],
)
def test_decimal(params, expected):
    result = Decimal(**params)

    assert result == expected


@pytest.mark.parametrize(
    "numerator, denominator, expected",
    [
        ("3", "2", True),
        ("2", "3", False),
    ],
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
    ],
)
def test_calculate_division(numerator, denominator, expected):
    result = _calculate_division(numerator, denominator)

    assert result == expected


@pytest.mark.parametrize(
    "numerator, denominator, fixed, repeating_decimal",
    [
        (Decimal(number="3.0"), Decimal(number="2.0"), "1.5", ""),
        (Decimal(number="1.0"), Decimal(number="3.0"), "0.", "3"),
        (Decimal(number="1.0"), Decimal(number="7.0"), "0.", "142857"),
        (Decimal(number="-3.0"), Decimal(number="2.0"), "-1.5", ""),
        (Decimal(number="1.0"), Decimal(number="-3.0"), "-0.", "3"),
        (Decimal(number="-1.0"), Decimal(number="-7.0"), "0.", "142857"),
    ],
    indirect=["repeating_decimal"],
)
def test_division(numerator, denominator, fixed, repeating_decimal):
    result = division(numerator, denominator)

    assert result == Decimal(number=(fixed + repeating_decimal))


@pytest.mark.parametrize(
    "number_1, number_2, expected",
    [
        (
            Decimal(number="33.3"),
            Decimal(number="2.222"),
            (Decimal(number="33.300"), Decimal(number="02.222")),
        ),
        (
            Decimal(number="3333.333333"),
            Decimal(number="0.0"),
            (Decimal(number="3333.333333"), Decimal(number="0000.000000")),
        ),
    ],
)
def test_match_number_sizes(number_1, number_2, expected):
    _match_number_sizes(number_1, number_2)

    assert (number_1, number_2) == expected


@pytest.mark.parametrize(
    "digit_1, digit_2, carry, expected",
    [
        (
            "2",
            "3",
            "0",
            ("0", "5"),
        ),
        (
            "2",
            "3",
            "3",
            ("0", "8"),
        ),
        (
            "2",
            "3",
            "4",
            ("0", "9"),
        ),
        (
            "2",
            "3",
            "6",
            ("1", "1"),
        ),
        (
            "9",
            "9",
            "9",
            ("2", "7"),
        ),
    ],
)
def test_add_string(digit_1, digit_2, carry, expected):
    result = _add_string(digit_1, digit_2, carry)

    assert result == expected


@pytest.mark.parametrize(
    "first, second, expected",
    [
        (
            Decimal(number="33.3"),
            Decimal(number="2.222"),
            Decimal(number="35.522"),
        ),
        (
            Decimal(number="22.222"),
            Decimal(number="0.0"),
            Decimal(number="22.222"),
        ),
        (
            Decimal(number="12.345"),
            Decimal(number="67.89"),
            Decimal(number="80.235"),
        ),
        (
            Decimal(number="-12.345"),
            Decimal(number="67.89"),
            Decimal(number="55.545"),
        ),
        (
            Decimal(number="67.89"),
            Decimal(number="-12.345"),
            Decimal(number="55.545"),
        ),
        (
            Decimal(number="-12.345"),
            Decimal(number="-67.89"),
            Decimal(number="-80.235"),
        ),
    ],
)
def test_add(first, second, expected):
    result = add(first, second)

    assert result == expected


@pytest.mark.parametrize(
    "digit_1, digit_2, borrow, returned, expected",
    [
        (
            "3",
            "2",
            "0",
            "0",
            ("1", "0"),
        ),
        (
            "4",
            "2",
            "0",
            "1",
            ("1", "0"),
        ),
        (
            "2",
            "3",
            "1",
            "0",
            ("9", "1"),
        ),
        (
            "2",
            "3",
            "1",
            "1",
            ("8", "1"),
        ),
    ],
)
def test_sub_string(digit_1, digit_2, borrow, returned, expected):
    result, next_returned = _sub_string(digit_1, digit_2, borrow, returned)

    assert (result, next_returned) == expected


@pytest.mark.parametrize(
    "first, second, expected",
    [
        (
            Decimal(number="33.3"),
            Decimal(number="2.222"),
            Decimal(number="31.078"),
        ),
        (
            Decimal(number="22.222"),
            Decimal(number="0.0"),
            Decimal(number="22.222"),
        ),
        (
            Decimal(number="12.345"),
            Decimal(number="67.89"),
            Decimal(number="-55.545"),
        ),
        (
            Decimal(number="-12.345"),
            Decimal(number="67.89"),
            Decimal(number="-80.235"),
        ),
        (
            Decimal(number="67.89"),
            Decimal(number="-12.345"),
            Decimal(number="80.235"),
        ),
        (
            Decimal(number="-12.345"),
            Decimal(number="-67.89"),
            Decimal(number="55.545"),
        ),
    ],
)
def test_sub(first, second, expected):
    result = sub(first, second)

    assert result == expected


@pytest.mark.parametrize(
    "first, second, expected",
    [
        (
            Decimal(number="33.3"),
            Decimal(number="2.222"),
            Decimal(number="73.9926"),
        ),
        (
            Decimal(number="0.0003"),
            Decimal(number="2.222"),
            Decimal(number="0.0006666"),
        ),
        (
            Decimal(number="-33.3"),
            Decimal(number="2.222"),
            Decimal(number="-73.9926"),
        ),
        (
            Decimal(number="33.3"),
            Decimal(number="-2.222"),
            Decimal(number="-73.9926"),
        ),
        (
            Decimal(number="-33.3"),
            Decimal(number="-2.222"),
            Decimal(number="73.9926"),
        ),
    ],
)
def test_multiplication(first, second, expected):
    result = multiplication(first, second)

    assert result == expected
