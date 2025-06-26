"""
The engineers seem concerned;
the total calibration result you gave them is nowhere close to being within safety tolerances.
Just then, you spot your mistake:
some well-hidden elephants are holding a third type of operator.

The concatenation operator (||)
combines the digits from its left and right inputs into a single number.
For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true
using only addition and multiplication,
the above example has three more equations that can be made true by inserting operators:

    156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
    7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
    192: 17 8 14 can be made true using 17 || 8 + 14.

Adding up all six test values
(the three that could be made before using only + and * plus the new three
that can now be made by also using ||)
produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots,
determine which equations could possibly be true.
What is their total calibration result?
"""

from collections.abc import Iterator
from enum import StrEnum
from itertools import chain, product, starmap, zip_longest
from operator import add, mul


class Operation(StrEnum):
    ADD = "+"
    MUL = "*"
    CONCAT = "|"


type Equation = list[int | Operation]


def find_correct_equations(
    total: int,
    operands: list[int],
) -> tuple[int, list[Equation]]:
    operations = combine_operations(n=len(operands) - 1)
    equations = interleave(operands, operations)
    return total, [eq for eq in equations if check_equation(total, eq)]


def check_equation(total: int, equation: Equation) -> bool:
    acc = 0
    last_operation = add

    for el in equation:
        match el:
            case int():
                acc = last_operation(acc, el)
            case Operation.ADD:
                last_operation = add
            case Operation.MUL:
                last_operation = mul
            case Operation.CONCAT:
                last_operation = concat

        if acc > total:
            break

    return acc == total


def combine_operations(
    n: int,
    operations: Operation = None,
) -> Iterator[list[Operation]]:
    if operations is None:
        operations = list(Operation)
    return product(operations, repeat=n)


def interleave(
    operands: list[int],
    operations: Iterator[list[Operation]],
) -> Iterator[list[Equation]]:
    for ops in operations:
        yield list(chain.from_iterable(zip_longest(operands, ops)))


def concat(a, b):
    return int(f"{a}{b}")


def pp(equations_with_total: tuple[int, list[Equation]]) -> tuple[int, list[str]]:
    total, equations = equations_with_total
    return total, ["".join(map(str, filter(bool, eq))) for eq in equations]


def join_chars(strs):
    return ["".join(chars) for chars in strs]


assert join_chars(combine_operations(2, "AB")) == ["AA", "AB", "BA", "BB"]
assert join_chars(combine_operations(2, "ABC")) == [
    "AA",
    "AB",
    "AC",
    "BA",
    "BB",
    "BC",
    "CA",
    "CB",
    "CC",
]
assert join_chars(interleave("AB", ["CD", "EF"])) == ["ACBD", "AEBF"]

assert pp(find_correct_equations(190, (10, 19))) == (190, ["10*19"])
assert pp(find_correct_equations(3267, (81, 40, 27))) == (
    3267,
    [("81+40*27"), ("81*40+27")],
)
assert find_correct_equations(83, (17, 5)) == (83, [])
assert pp(find_correct_equations(156, (15, 6))) == (156, ["15|6"])
assert pp(find_correct_equations(7290, (6, 8, 6, 15))) == (7290, ["6*8|6*15"])
assert find_correct_equations(161011, (16, 10, 13)) == (161011, [])
assert pp(find_correct_equations(192, (17, 8, 14))) == (192, ["17|8+14"])
assert find_correct_equations(21037, (9, 7, 18, 13)) == (21037, [])
assert pp(find_correct_equations(292, (11, 6, 16, 20))) == (292, ["11+6*16+20"])


def parse(raw_str):
    total, raw_operands = raw_str.split(":")
    operands = raw_operands.strip().split(" ")
    return int(total), list(map(int, operands))


with open("2024/07_bridge_repair/input.txt") as f:
    correct_equations = starmap(find_correct_equations, map(parse, f))
    print(sum(res for res, equations in correct_equations if equations))
