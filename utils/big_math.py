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
        self.decimal = self.decimal[:DECIMAL_LIMIT]

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
        cleaned_whole = self.whole.lstrip("0").split(".")
        self.whole = cleaned_whole[0] if cleaned_whole[0] else "0"
        left = "".join(cleaned_whole[1:]) if len(cleaned_whole) > 1 else ""
        cleaned_decimal = (left + self.decimal).rstrip("0").replace(".", "")
        self.decimal = cleaned_decimal if cleaned_decimal else "0"
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
    num, den = Decimal(**numerator.__dict__), Decimal(**denominator.__dict__)
    result_negative = False
    if (
        num.is_negative
        and not den.is_negative
        or not num.is_negative
        and den.is_negative
    ):
        result_negative = True

    result, remainder = Decimal(), ""
    _match_number_sizes(num, den)
    num.number, den.number = (
        num.number.replace(".", ""),
        den.number.replace(".", ""),
    )
    num.update_decimal()
    den.update_decimal()

    for number in _get_num(num.number):
        result.whole, remainder = _generate_result(
            remainder, number, den.number, result.whole
        )

    result.decimal = ""
    while len(result.decimal) < DECIMAL_LIMIT and remainder != "0":
        result.decimal, remainder = _generate_result(
            remainder, "0", den.number, result.decimal
        )

    result.is_negative = result_negative
    result.update_number()
    result.clean_number()
    return result


def _get_num(num: str) -> Generator[str, None, None]:
    for char in num:
        yield char


def _generate_result(
    remainder: str,
    increment: str,
    den: str,
    result: str,
) -> Tuple[str, str]:
    remainder += increment

    if _fits(remainder, den):
        partial_result, remainder = _calculate_division(remainder, den)
        result += partial_result
    else:
        result += "0"

    return result, remainder


def _calculate_division(num: str, den: str) -> Tuple[str, str]:
    return str(int(num) // int(den)), str(int(num) % int(den))


def _fits(num: str, den: str) -> bool:
    return bool(float(num) // float(den))


def add(first: Decimal, second: Decimal) -> Decimal:
    st, nd = Decimal(**first.__dict__), Decimal(**second.__dict__)
    if st.is_negative and not nd.is_negative:
        st.is_negative = False
        return sub(nd, st)
    elif not st.is_negative and nd.is_negative:
        nd.is_negative = False
        return sub(st, nd)

    result_negative = st.is_negative and nd.is_negative
    result_number = ""
    _match_number_sizes(st, nd)
    carry = "0"
    for digit_1, digit_2 in zip(reversed(st.number), reversed(nd.number)):
        if digit_1 == ".":
            result_number = "." + result_number
            continue
        carry, partial_result = _add_string(digit_1, digit_2, carry)
        result_number = partial_result + result_number

    result = Decimal(number=carry + result_number, is_negative=result_negative)
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
    st, nd = Decimal(**first.__dict__), Decimal(**second.__dict__)
    if st.is_negative and not nd.is_negative:
        nd.is_negative = True
        return add(nd, st)
    elif not st.is_negative and nd.is_negative:
        nd.is_negative = False
        return add(st, nd)

    returned, result_number, result_negative = "0", "", False
    _match_number_sizes(st, nd)
    if float(st.number) < float(nd.number):
        st, nd = nd, st
        if not st.is_negative and not nd.is_negative:
            result_negative = True

    for digit_1, digit_2 in zip(reversed(st.number), reversed(nd.number)):
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
    mpc, mpl = Decimal(**multiplicand.__dict__), Decimal(**multiplier.__dict__)
    result_negative = False
    if (
        mpc.is_negative
        and not mpl.is_negative
        or not mpc.is_negative
        and mpl.is_negative
    ):
        result_negative = True

    decimal_places = 2 * max(len(mpc.decimal), len(mpl.decimal))
    _match_number_sizes(mpc, mpl)
    mpc.number, mpl.number = (
        mpc.number.replace(".", ""),
        mpl.number.replace(".", ""),
    )
    mpc.update_decimal()
    mpl.update_decimal()
    result, partial_result, partial_innter_result = Decimal(), [], []

    for shift, digit_2 in enumerate(reversed(mpl.number)):
        outer_result = Decimal()
        for inner_shift, digit_1 in enumerate(reversed(mpc.number)):
            inner_result = Decimal()
            for _ in range(int(digit_2)):
                inner_result = add(inner_result, Decimal(number=digit_1))
            partial_innter_result.append(inner_result.whole + inner_shift * "0")
        for number in partial_innter_result:
            outer_result = add(outer_result, Decimal(number=number))
        outer_result.whole = outer_result.whole + shift * "0"
        outer_result.update_number()
        partial_result.append(outer_result)
        partial_innter_result.clear()

    for number in partial_result:
        result = add(result, number)

    result.is_negative = result_negative
    result.whole = decimal_places * "0" + result.whole
    result.whole = result.whole[:-decimal_places] + "." + result.whole[-decimal_places:]
    result.clean_number()
    result.update_number()
    return result


def power(base: Decimal, exponent: str):
    bs = Decimal(**base.__dict__)
    result = Decimal(number="1")
    if exponent == "0":
        return result
    for _ in range(int(exponent)):
        result = multiplication(result, bs)

    return result


def arctan_1_x(number: Decimal) -> str:
    step = 0
    operation = {
        "0": add,
        "1": sub,
    }
    result, partial_result = Decimal(), Decimal()
    while True:
        op = str(step % 2)
        coefficient = str(2 * step + 1)
        p = power(number, coefficient)
        m = multiplication(Decimal(number=coefficient), p)
        d = division(Decimal(number="1"), m)
        partial_result = operation[op](result, d)
        difference = sub(result, partial_result)
        if (
            difference.number[:DECIMAL_LIMIT]
            == f"0.{DECIMAL_LIMIT * '0'}"[:DECIMAL_LIMIT]
        ):
            return partial_result
        result = partial_result
        step += 1
