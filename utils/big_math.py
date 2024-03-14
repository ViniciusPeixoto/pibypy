import os
from typing import Generator, Tuple

DECIMAL_LIMIT = int(os.getenv("DECIMAL_LIMIT", "10"))


def division(numerator: str, denominator: str) -> str:
    result, remainder = "", ""

    for number in _get_numerator(numerator):
        result, remainder = _generate_result(remainder, number, denominator, result)

    if not result:
        result = "0."
    else:
        result += "."

    while len(result.split(".")[1]) < DECIMAL_LIMIT and remainder != "0":
        result, remainder = _generate_result(remainder, "0", denominator, result)

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
            result += partial_result

        return result, remainder


def _calculate_division(numerator: str, denominator: str) -> Tuple[str, str]:
    return str(int(numerator) // int(denominator)), str(int(numerator) % int(denominator))


def _fits(numerator: str, denominator: str) -> bool:
    return bool(int(numerator) // int(denominator))
