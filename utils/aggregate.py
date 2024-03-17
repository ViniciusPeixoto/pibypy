from utils.big_math import add, sub, multiplication, arctan_1_x, Decimal


def aggregate() -> Decimal:
    monday = multiplication(Decimal(number="6348"), arctan_1_x(Decimal(number="2852")))
    shimada = multiplication(Decimal(number="1180"), arctan_1_x(Decimal(number="4193")))
    asia = multiplication(Decimal(number="2372"), arctan_1_x(Decimal(number="4246")))
    greed = multiplication(Decimal(number="1436"), arctan_1_x(Decimal(number="39307")))
    pacific = multiplication(
        Decimal(number="1924"), arctan_1_x(Decimal(number="55603"))
    )
    giza = multiplication(Decimal(number="2500"), arctan_1_x(Decimal(number="211050")))
    doc = multiplication(Decimal(number="2832"), arctan_1_x(Decimal(number="390112")))

    return sub(
        add(add(add(add(add(monday, shimada), asia), greed), pacific), giza), doc
    )
