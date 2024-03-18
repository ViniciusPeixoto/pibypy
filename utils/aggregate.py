import logging
from functools import partial
from multiprocessing import get_context
from typing import Callable

from utils.big_math import add, sub, multiplication, arctan_1_x, Decimal

logger = logging.getLogger(__name__)
logging.basicConfig(filename="logs/pilog.log", level=logging.INFO)


def calculate_monday():
    logger.info("Calculating Monday...")
    return {
        "monday": multiplication(
            Decimal(number="6348"), arctan_1_x(Decimal(number="2852"), "monday")
        )
    }


def calculate_shimada():
    logger.info("Calculating Shimada...")
    return {
        "shimada": multiplication(
            Decimal(number="1180"), arctan_1_x(Decimal(number="4193"), "shimada")
        )
    }


def calculate_asia():
    logger.info("Calculating Asia...")
    return {
        "asia": multiplication(
            Decimal(number="2372"), arctan_1_x(Decimal(number="4246"), "asia")
        )
    }


def calculate_greed():
    logger.info("Calculating Greed...")
    return {
        "greed": multiplication(
            Decimal(number="1436"), arctan_1_x(Decimal(number="39307"), "greed")
        )
    }


def calculate_pacific():
    logger.info("Calculating Pacific...")
    return {
        "pacific": multiplication(
            Decimal(number="1924"), arctan_1_x(Decimal(number="55603"), "pacific")
        )
    }


def calculate_giza():
    logger.info("Calculating Giza...")
    return {
        "giza": multiplication(
            Decimal(number="2500"), arctan_1_x(Decimal(number="211050"), "giza")
        )
    }


def calculate_doc():
    logger.info("Calculating Doc...")

    return {
        "doc": multiplication(
            Decimal(number="2832"), arctan_1_x(Decimal(number="390112"), "doc")
        )
    }


def operations() -> dict:
    return {
        "monday": calculate_monday,
        "shimada": calculate_shimada,
        "asia": calculate_asia,
        "greed": calculate_greed,
        "pacific": calculate_pacific,
        "giza": calculate_giza,
        "doc": calculate_doc,
    }


def operation(name: str) -> Callable:
    logger.info(f"Starting operation: {name}")
    result = operations().get(name)()
    logger.info(f"Operation {name}: done")
    return result


def map_operation(f: Callable) -> Callable:
    return f()


def aggregate() -> Decimal:
    results = {}
    logger.info("Starting calculations...")

    op_list = [
        partial(calculate_monday),
        partial(calculate_shimada),
        partial(calculate_asia),
        partial(calculate_greed),
        partial(calculate_pacific),
        partial(calculate_giza),
        partial(calculate_doc),
    ]

    with get_context("spawn").Pool(processes=3) as pool:
        logger.info("Initializing operations...")
        op_results = pool.imap_unordered(map_operation, op_list)

        for result in op_results:
            results.update(result)

            logger.info(f"Gathering results for {next(iter(result))}: done")

    # for op in ops:
    #     logger.info(f"Gathering results from {op}")
    #     results.update(operation(op))
    #     logger.info(f"Gathering results from {op}: done")

    return sub(
        add(
            add(
                add(
                    add(
                        add(results.get("monday"), results.get("shimada")),
                        results.get("asia"),
                    ),
                    results.get("greed"),
                ),
                results.get("pacific"),
            ),
            results.get("giza"),
        ),
        results.get("doc"),
    )
