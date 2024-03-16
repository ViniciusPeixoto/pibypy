import pytest

from utils.big_math import DECIMAL_LIMIT


@pytest.fixture
def repeating_decimal(request):
    return (
        (str(request.param) * (DECIMAL_LIMIT // len(str(request.param)) + 1))[
            :DECIMAL_LIMIT
        ]
        if str(request.param)
        else ""
    )
