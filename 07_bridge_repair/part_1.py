"""
The Historians take you to a familiar rope bridge over a river in the middle of a jungle.
The Chief isn't on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it.
(Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations,
but some young elephants were playing nearby and stole all the operators
from their calibration equations! They could finish the calibrations
if only someone could determine which test values could possibly be produced
by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20

Each line represents a single equation.
The test value appears before the colon on each line;
it is your job to determine whether the remaining numbers can be combined with operators
to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules.
Furthermore, numbers in the equations cannot be rearranged.
Glancing into the jungle, you can see elephants
holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

    190: 10 19 has only one position that accepts an operator: between 10 and 19.
         Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
    3267: 81 40 27 has two positions for operators.
          Of the four possible configurations of the operators,
          two cause the right side to match the test value:
          81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
    292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

The engineers just need the total calibration result,
which is the sum of the test values from just the equations
that could possibly be true.
In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?
"""

from collections.abc import Iterator
from enum import StrEnum
from itertools import chain, product, starmap, zip_longest
from operator import add, mul


class Operation(StrEnum):
    ADD = "+"
    MUL = "*"


type Equation = list[int | Operation]


def find_correct_equations(
    total: int,
    operands: list[int],
) -> tuple[int, list[Equation]]:
    operations = get_possible_operations(n=len(operands) - 1)
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

        if acc > total:
            break

    return acc == total


def get_possible_operations(
    n: int,
    operations: Operation = (Operation.ADD, Operation.MUL),
) -> Iterator[list[Operation]]:
    return product(operations, repeat=n)


def interleave(
    operands: list[int],
    operations: Iterator[list[Operation]],
) -> Iterator[list[Equation]]:
    for ops in operations:
        yield list(chain.from_iterable(zip_longest(operands, ops)))


def pp(equations_with_total: tuple[int, list[Equation]]) -> tuple[int, list[str]]:
    total, equations = equations_with_total
    return total, ["".join(map(str, filter(bool, eq))) for eq in equations]


def join_chars(strs):
    return ["".join(chars) for chars in strs]


assert join_chars(get_possible_operations(2, "AB")) == ["AA", "AB", "BA", "BB"]
assert join_chars(interleave("AB", ["CD", "EF"])) == ["ACBD", "AEBF"]

assert pp(find_correct_equations(190, (10, 19))) == (190, ["10*19"])
assert pp(find_correct_equations(3267, (81, 40, 27))) == (
    3267,
    [("81+40*27"), ("81*40+27")],
)
assert find_correct_equations(83, (17, 5)) == (83, [])
assert find_correct_equations(156, (15, 6)) == (156, [])
assert find_correct_equations(7290, (6, 8, 6, 15)) == (7290, [])
assert find_correct_equations(161011, (16, 10, 13)) == (161011, [])
assert find_correct_equations(192, (17, 8, 14)) == (192, [])
assert find_correct_equations(21037, (9, 7, 18, 13)) == (21037, [])
assert pp(find_correct_equations(292, (11, 6, 16, 20))) == (292, ["11+6*16+20"])


def parse(raw_str):
    total, raw_operands = raw_str.split(":")
    operands = raw_operands.strip().split(" ")
    return int(total), list(map(int, operands))


with open("07_bridge_repair/input.txt") as f:
    correct_equations = starmap(find_correct_equations, map(parse, f))
    print(sum(res for res, equations in correct_equations if equations))
