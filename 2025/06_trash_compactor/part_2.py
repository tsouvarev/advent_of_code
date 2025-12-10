"""
The big cephalopods come back to check on how things are going.
When they see that your grand total doesn't match the one expected by the worksheet,
they realize they forgot to explain how to read cephalopod math.

Cephalopod math is written right-to-left in columns.
Each number is given in its own column,
with the most significant digit at the top
and the least significant digit at the bottom.
(Problems are still separated with a column consisting only of spaces,
and the symbol at the bottom of the problem is still the operator to use.)

Here's the example worksheet again:

123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +

Reading the problems right-to-left one column at a time,
the problems are now quite different:

    The rightmost problem is 4 + 431 + 623 = 1058
    The second problem from the right is 175 * 581 * 32 = 3253600
    The third problem from the right is 8 + 248 + 369 = 625
    Finally, the leftmost problem is 356 * 24 * 1 = 8544

Now, the grand total is 1058 + 3253600 + 625 + 8544 = 3263827.

Solve the problems on the math worksheet again.
What is the grand total
found by adding together all of the answers to the individual problems?
"""

import re
from collections.abc import Iterable
from enum import StrEnum
from functools import reduce
from itertools import groupby
from operator import mul
from typing import NamedTuple

type Sheet = list[Problem]


class Problem(NamedTuple):
    op: Op
    numbers: list[int]


class Op(StrEnum):
    ADD = "+"
    MUL = "*"


def get_total(sheet: Sheet) -> int:
    res = 0

    for problem in sheet:
        match problem.op:
            case Op.ADD:
                res += sum(problem.numbers)
            case Op.MUL:
                res += reduce(mul, problem.numbers, 1)
            case _:
                raise ValueError
    return res


def _parse_sheet(f: Iterable[str]) -> Sheet:
    *digits, raw_ops = f

    numbers = map(_maybe_int, zip(*digits))
    ops = map(Op, re.split(r"\s+", raw_ops.strip()))

    res = []

    for sep, args in groupby(numbers, key=lambda n: n is not None):
        if sep:
            res.append(Problem(next(ops), list(args)))
    return res


def _maybe_int(chars: tuple[str]) -> int | None:
    try:
        return int("".join(chars).strip())
    except ValueError:
        return None


f = [
    "13",
    "2 ",
    "+ ",
]
assert _parse_sheet(f) == [Problem(Op.ADD, [12, 3])]

f = [
    "1 ",
    "23",
    "+ ",
]
assert _parse_sheet(f) == [Problem(Op.ADD, [12, 3])]

f = [
    "1  12",
    "23  2",
    "+  * ",
]
assert _parse_sheet(f) == [Problem(Op.ADD, [12, 3]), Problem(Op.MUL, [1, 22])]

f = [
    "123 328  51 64 ",
    " 45 64  387 23 ",
    "  6 98  215 314",
    "*   +   *   +  ",
]
assert get_total(_parse_sheet(f)) == 3263827


with open("2025/06_trash_compactor/input.txt") as f:
    sheet = _parse_sheet(f)
    print(get_total(sheet))
