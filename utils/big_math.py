import os
from typing import Generator, Tuple

DECIMAL_LIMIT = int(os.getenv("DECIMAL_LIMIT", "10"))


class Decimal:
    def __init__(self, **kwargs) -> None:
        self.number = kwargs.get("number")
        self.whole = kwargs.get("whole")
        self.decimal = kwargs.get("decimal")
        self.is_negative = kwargs.get("is_negative")
        if self.number:
            if self.is_negative is None:
                self.is_negative = self.number[0] == "-"
            self.number = self.number.lstrip("-")
            self.update_decimal()
        elif self.whole and self.decimal:
            if self.is_negative is None:
                self.is_negative = self.whole[0] == "-"
            self.whole = self.whole.lstrip("-")
            self.update_number()
        else:
            self.number = "0.0"
            self.whole = "0"
            self.decimal = "0"
            self.is_negative = False

    def __eq__(self, other: object) -> bool:
        return all(
            float(getattr(self, attr)) == float(getattr(other, attr))
            for attr in self.__dict__
        )

    def update_decimal(self):
        try:
            whole = self.number.split(".")[0]
            self.whole = whole if whole else "0"
            decimal = self.number.split(".")[1]
            self.decimal = decimal if decimal else "0"
        except IndexError:
            self.whole = self.number
            self.decimal = "0"

    def update_number(self):
        self.number = f"{self.whole if self.whole else '0'}.{self.decimal if self.decimal else '0'}"

    def clean_number(self):
        cleaned_decimal = self.decimal.rstrip("0")
        self.decimal = cleaned_decimal if cleaned_decimal else "0"
        cleaned_whole = self.whole.lstrip("0")
        self.whole = cleaned_whole if cleaned_whole else "0"
        self.number = f"{self.whole}.{self.decimal}"

    def match_size(self, other):
        self.whole = self.whole.zfill(len(other.whole))
        self.decimal = self.decimal.ljust(len(other.decimal), "0")
        self.update_number()

    def get_number(self) -> str:
        return f"{self.is_negative * '-'}{self.whole}.{self.decimal}"

    def get_unsigned_number(self):
        return self.get_number().lstrip("-")

    def get_whole(self) -> str:
        return f"{self.is_negative * '-'}{self.whole}"

    def get_decimal(self) -> str:
        return self.decimal

    def get_negative(self) -> bool:
        return self.is_negative


def division(numerator: Decimal, denominator: Decimal) -> Decimal:
    result_negative = False
    if (
        numerator.is_negative
        and not denominator.is_negative
        or not numerator.is_negative
        and denominator.is_negative
    ):
        result_negative = True

    result, remainder = Decimal(), ""
    _match_number_sizes(numerator, denominator)
    numerator.number, denominator.number = (
        numerator.number.replace(".", ""),
        denominator.number.replace(".", ""),
    )
    numerator.update_decimal()
    denominator.update_decimal()

    for number in _get_numerator(numerator.number):
        result.whole, remainder = _generate_result(
            remainder, number, denominator.number, result.whole
        )

    while len(result.decimal) < DECIMAL_LIMIT and remainder != "0":
        result.decimal, remainder = _generate_result(
            remainder, "0", denominator.number, result.decimal
        )

    result.is_negative = result_negative
    result.update_number()
    result.clean_number()
    return result


def _get_numerator(numerator: str) -> Generator[str, None, None]:
    for char in numerator:
        yield char


def _generate_result(
    remainder: str,
    increment: str,
    denominator: str,
    result: str,
) -> Tuple[str, str]:
    remainder += increment

    if _fits(remainder, denominator):
        partial_result, remainder = _calculate_division(remainder, denominator)
        if result == "0":
            result = partial_result
        else:
            result += partial_result

    return result, remainder


def _calculate_division(numerator: str, denominator: str) -> Tuple[str, str]:
    return str(int(numerator) // int(denominator)), str(
        int(numerator) % int(denominator)
    )


def _fits(numerator: str, denominator: str) -> bool:
    return bool(float(numerator) // float(denominator))


def add(first: Decimal, second: Decimal) -> Decimal:
    if first.is_negative and not second.is_negative:
        first.is_negative = False
        return sub(second, first)
    elif not first.is_negative and second.is_negative:
        second.is_negative = False
        return sub(first, second)

    result_negative = first.is_negative and second.is_negative
    result_number = ""
    _match_number_sizes(first, second)
    carry = "0"
    for digit_1, digit_2 in zip(reversed(first.number), reversed(second.number)):
        if digit_1 == ".":
            result_number = "." + result_number
            continue
        carry, partial_result = _add_string(digit_1, digit_2, carry)
        result_number = partial_result + result_number

    result = Decimal(number=result_number, is_negative=result_negative)
    result.clean_number()
    return result


def _add_string(digit_1: str, digit_2: str, carry: str) -> str:
    return tuple(
        digit for digit in str(int(digit_1) + int(digit_2) + int(carry)).zfill(2)
    )


def _match_number_sizes(number_1: Decimal, number_2: Decimal) -> None:
    number_1.match_size(number_2)
    number_2.match_size(number_1)


def _sub_string(digit_1: str, digit_2: str, borrow: str, returned: str) -> str:
    return str(int(borrow + digit_1) - int(digit_2) - int(returned)), borrow


def sub(first: Decimal, second: Decimal) -> Decimal:
    if first.is_negative and not second.is_negative:
        second.is_negative = True
        return add(second, first)
    elif not first.is_negative and second.is_negative:
        second.is_negative = False
        return add(first, second)

    returned, result_number, result_negative = "0", "", False
    _match_number_sizes(first, second)
    if float(first.number) < float(second.number):
        first, second = second, first
        if not first.is_negative and not second.is_negative:
            result_negative = True

    for digit_1, digit_2 in zip(reversed(first.number), reversed(second.number)):
        if digit_1 == ".":
            result_number = "." + result_number
            continue
        borrow = "1" if int(digit_1) < int(digit_2) + int(returned) else "0"
        partial_result, returned = _sub_string(digit_1, digit_2, borrow, returned)
        result_number = partial_result + result_number

    result = Decimal(number=result_number, is_negative=result_negative)
    result.clean_number()
    return result


def multiplication(multiplicand: Decimal, multiplier: Decimal) -> Decimal:
    pass


def power(base: Decimal, exponent: str):
    pass


def arctan_1_x(number: str) -> str:
    result = Decimal()
    step = 0
    operation = {
        "0": add,
        "1": sub,
    }
    while len(result.decimal) < DECIMAL_LIMIT:
        op = str(step % 2)
        coefficient = 2 * step + 1
        result = operation[op](
            result,
            division(
                Decimal(whole="1"),
                multiplication(
                    Decimal(whole=coefficient),
                    power(Decimal(number=number), str(coefficient)),
                ),
            ),
        )
