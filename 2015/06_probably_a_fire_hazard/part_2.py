"""
You just finish implementing your winning light pattern
when you realize you mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls;
each light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means
that you should increase the brightness of those lights by 1.

The phrase turn off actually means
that you should decrease the brightness of those lights by 1, to a minimum of zero.

The phrase toggle actually means
that you should increase the brightness of those lights by 2.

What is the total brightness
of all lights combined after following Santa's instructions?

For example:
- turn on 0,0 through 0,0 would increase the total brightness by 1.
- toggle 0,0 through 999,999 would increase the total brightness by 2000000.

"""

import re
from enum import StrEnum, auto
from textwrap import dedent
from typing import NamedTuple

type Field = list[list[int]]


class Coord(NamedTuple):
    x: int
    y: int


class Action(StrEnum):
    ON = auto()
    OFF = auto()
    TOGGLE = auto()


def change_brightness(field: Field, from_: Coord, to_: Coord, action: Action) -> Field:
    for i in range(from_.x, to_.x + 1):
        for j in range(from_.y, to_.y + 1):
            match action:
                case Action.TOGGLE:
                    field[i][j] += 2
                case Action.ON:
                    field[i][j] += 1
                case Action.OFF:
                    field[i][j] = max(0, field[i][j] - 1)
    return field


def count_brightness(field: Field) -> int:
    res = 0

    for row in field:
        for col in row:
            res += col

    return res


def _generate_field(size_x: int, size_y: int) -> Field:
    return [[False] * size_y for _ in range(size_x)]


def _to_array(s: str) -> Field:
    return [list(map(int, line)) for line in dedent(s).strip().splitlines()]


def _to_map(field: Field) -> str:
    return "\n".join("".join(map(str, row)) for row in field)


def _check_switch(
    raw_field: str,
    from_: tuple[int, int],
    to_: tuple[int, int],
    action: Action,
) -> str:
    mapped = _to_map(
        change_brightness(_to_array(raw_field), Coord(*from_), Coord(*to_), action),
    )
    return f"\n{mapped}"


field = """
    000
    000
    000
    """
assert _check_switch(field, (0, 0), (1, 1), Action.ON) == dedent(
    """
    110
    110
    000
    """,
)

field = """
    110
    110
    000
    """
assert _check_switch(field, (0, 0), (1, 1), Action.OFF) == dedent(
    """
    000
    000
    000
    """,
)

field = """
    000
    000
    000
    """
assert _check_switch(field, (0, 0), (1, 1), Action.OFF) == dedent(
    """
    000
    000
    000
    """,
)

field = """
    000
    000
    000
    """
assert _check_switch(field, (0, 0), (1, 1), Action.TOGGLE) == dedent(
    """
    220
    220
    000
    """,
)

field = _to_array(
    """
    012
    012
    000
    """,
)
assert count_brightness(field) == 6


with open("2015/06_probably_a_fire_hazard/input.txt") as f:
    field = _generate_field(1000, 1000)

    for line in f:
        from_x, from_y, to_x, to_y = map(int, re.findall(r"\d+", line))
        from_, to_ = Coord(from_x, from_y), Coord(to_x, to_y)

        if line.startswith("toggle"):
            field = change_brightness(field, from_, to_, Action.TOGGLE)
        elif line.startswith("turn off"):
            field = change_brightness(field, from_, to_, Action.OFF)
        elif line.startswith("turn on"):
            field = change_brightness(field, from_, to_, Action.ON)

    print(count_brightness(field))
