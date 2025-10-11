"""
You come across a door implementing what you can only assume
is an implementation of two-factor authentication
after a long game of requirements telephone.

To get past the door, you first swipe a keycard
(no problem; there was one on a nearby desk).
Then, it displays a code on a little screen, and you type that code on a keypad.
Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed.
After a few minutes, you've taken everything apart and figured out how it works.
Now you just have to work out what the screen would have displayed.

The magnetic strip on the card you swiped
encodes a series of instructions for the screen;
these instructions are your puzzle input.
The screen is 50 pixels wide and 6 pixels tall, all of which start off,
and is capable of three somewhat peculiar operations:

-   rect AxB turns on all of the pixels in a rectangle
    at the top-left of the screen which is A wide and B tall.
-   rotate row y=A by B shifts all of the pixels in row A (0 is the top row)
    right by B pixels. Pixels that would fall off the right end
    appear at the left end of the row.
-   rotate column x=A by B shifts all of the pixels in column A (0 is the left column)
    down by B pixels. Pixels that would fall off the bottom
    appear at the top of the column.

For example, here is a simple sequence on a smaller screen:

- rect 3x2 creates a small rectangle in the top-left corner:

###....
###....
.......

- rotate column x=1 by 1 rotates the second column down by one pixel:

#.#....
###....
.#.....

- rotate row y=0 by 4 rotates the top row right by four pixels:

....#.#
###....
.#.....

- rotate column x=1 by 1 again rotates the second column down by one pixel,
  causing the bottom pixel to wrap back to the top:

.#..#.#
#.#....
.#.....

As you can see, this display technology is extremely powerful,
and will soon dominate the tiny-code-displaying-screen market.
That's what the advertisement on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the display:
after you swipe your card, if the screen did work, how many pixels should be lit?
"""

from textwrap import dedent
from typing import NamedTuple

from parse import parse

type Field = list[list[bool]]
type Instruction = RectData | RotateColumnXData | RotateRowYData


class RectData(NamedTuple):
    x: int
    y: int


class RotateColumnXData(NamedTuple):
    x: int
    n: int


class RotateRowYData(NamedTuple):
    y: int
    n: int


def follow(x: int, y: int, instructions: list[Instruction]) -> Field:
    field = _generate_field(x, y)

    for i in instructions:
        match i:
            case RectData():
                field = _rect(field, i.x, i.y)
            case RotateColumnXData():
                field = _rotate_column_x(field, i.x, i.n)
            case RotateRowYData():
                field = _rotate_row_y(field, i.y, i.n)
            case _:
                raise ValueError(i)

    return field


def _generate_field(size_x: int, size_y: int) -> Field:
    return [[False] * size_x for _ in range(size_y)]


def _rect(field: Field, x: int, y: int) -> Field:
    for j in range(x):
        for i in range(y):
            field[i][j] = True
    return field


def _rotate_column_x(field: Field, x: int, n: int) -> Field:
    base = len(field)
    new_col = [field[(base + i - n) % base][x] for i in range(base)]

    for i in range(base):
        field[i][x] = new_col[i]

    return field


def _rotate_row_y(field: Field, y: int, n: int) -> Field:
    base = len(field[y])
    new_row = [field[y][(base + j - n) % base] for j in range(base)]
    field[y] = new_row
    return field


def count_lights(field: Field) -> int:
    lights = 0
    for row in field:
        for col in row:
            if col:
                lights += 1
    return lights


def _to_array(s: str) -> Field:
    return [[l == "#" for l in line] for line in dedent(s).strip().splitlines()]


def _to_map(field: Field) -> str:
    res = ""

    for row in field:
        for col in row:
            res += "#" if col else "."
        res += "\n"

    return res


field = _to_array(
    """
    .......
    .......
    .......
    """,
)
assert _rect(field, 3, 2) == _to_array(
    """
    ###....
    ###....
    .......
    """,
)

field = _to_array(
    """
    ###....
    ###....
    .......
    """,
)
assert _rotate_column_x(field, 1, 1) == _to_array(
    """
    #.#....
    ###....
    .#.....
    """,
)

field = _to_array(
    """
    ....#.#
    ###....
    .#.....
    """,
)
assert _rotate_column_x(field, 1, 1) == _to_array(
    """
    .#..#.#
    #.#....
    .#.....
    """,
)

field = _to_array(
    """
    #.#....
    ###....
    .#.....
    """,
)
assert _rotate_row_y(field, 0, 1) == _to_array(
    """
    .#.#...
    ###....
    .#.....
    """,
)

field = _to_array(
    """
    #.#....
    ###....
    .#.....
    """,
)
assert _rotate_row_y(field, 0, 4) == _to_array(
    """
    ....#.#
    ###....
    .#.....
    """,
)

field = _to_array(
    """
    #......
    ...#...
    ......#
    """,
)
assert count_lights(field) == 3


with open("2016/08_two_factor_authentication/input.txt") as f:
    instructions = []

    for line in f:
        if res := parse("rect {x:d}x{y:d}", line.strip()):
            instructions.append(RectData(**res.named))
        elif res := parse("rotate row y={y:d} by {n:d}", line.strip()):
            instructions.append(RotateRowYData(**res.named))
        elif res := parse("rotate column x={x:d} by {n:d}", line.strip()):
            instructions.append(RotateColumnXData(**res.named))
        else:
            raise ValueError(line)

    field = follow(50, 6, instructions)

    print(count_lights(field))
    print(_to_map(field), "\n")
