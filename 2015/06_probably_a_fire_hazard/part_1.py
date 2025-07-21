"""
Because your neighbors keep defeating you
in the holiday house decorating contest year after year,
you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year,
Santa has mailed you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction;
the lights at each corner are at 0,0, 0,999, 999,999, and 999,0.
The instructions include whether to turn on, turn off,
or toggle various inclusive ranges given as coordinate pairs.
Each coordinate pair represents opposite corners of a rectangle, inclusive;
a coordinate pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3 square.
The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights
by doing the instructions Santa sent you in order.

For example:
-   turn on 0,0 through 999,999 would turn on (or leave on) every light.
-   toggle 0,0 through 999,0 would toggle the first line of 1000 lights,
    turning off the ones that were on, and turning on the ones that were off.
-   turn off 499,499 through 500,500 would turn off (or leave off)
    the middle four lights.

After following the instructions, how many lights are lit?
"""

import re
from enum import StrEnum, auto
from textwrap import dedent
from typing import NamedTuple

type Field = list[list[bool]]


class Coord(NamedTuple):
    x: int
    y: int


class Action(StrEnum):
    ON = auto()
    OFF = auto()
    TOGGLE = auto()


def switch_lights(field: Field, from_: Coord, to_: Coord, action: Action):
    for i in range(from_.x, to_.x + 1):
        for j in range(from_.y, to_.y + 1):
            match action:
                case Action.TOGGLE:
                    field[i][j] = not field[i][j]
                case Action.ON:
                    field[i][j] = True
                case Action.OFF:
                    field[i][j] = False
    return field


def count_lights(field: Field) -> int:
    res = 0

    for row in field:
        for col in row:
            if col:
                res += 1

    return res


def _generate_field(size_x: int, size_y: int) -> Field:
    return [[False] * size_y for _ in range(size_x)]


def _to_array(s: str) -> Field:
    return [[l == "*" for l in line] for line in dedent(s).strip().splitlines()]


def _to_map(field: Field) -> str:
    res = ""

    for row in field:
        for col in row:
            res += "*" if col else "."
        res += "\n"

    return res


def _check_switch(
    raw_field: str,
    from_: tuple[int, int],
    to_: tuple[int, int],
    action: Action,
) -> str:
    mapped = _to_map(
        switch_lights(_to_array(raw_field), Coord(*from_), Coord(*to_), action),
    )
    return f"\n{mapped}"


field = """
    ...
    ...
    ...
    """
assert _check_switch(field, (0, 0), (1, 1), Action.ON) == dedent(
    """
    **.
    **.
    ...
    """,
)

field = """
    **.
    **.
    ...
    """
assert _check_switch(field, (0, 0), (1, 1), Action.OFF) == dedent(
    """
    ...
    ...
    ...
    """,
)

field = """
    .*.
    .*.
    ...
    """
assert _check_switch(field, (0, 0), (1, 1), Action.TOGGLE) == dedent(
    """
    *..
    *..
    ...
    """,
)

field = _to_array(
    """
    .*.
    .*.
    ...
    """,
)
assert count_lights(field) == 2


with open("2015/06_probably_a_fire_hazard/input.txt") as f:
    field = _generate_field(1000, 1000)

    for line in f:
        from_x, from_y, to_x, to_y = map(int, re.findall(r"\d+", line))
        from_, to_ = Coord(from_x, from_y), Coord(to_x, to_y)

        if line.startswith("toggle"):
            field = switch_lights(field, from_, to_, Action.TOGGLE)
        elif line.startswith("turn off"):
            field = switch_lights(field, from_, to_, Action.OFF)
        elif line.startswith("turn on"):
            field = switch_lights(field, from_, to_, Action.ON)

    print(count_lights(field))
