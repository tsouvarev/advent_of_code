"""
With your analysis of the manifold complete, you begin fixing the teleporter.
However, as you open the side of the teleporter to replace the broken manifold,
you are surprised to discover that it isn't a classical tachyon manifold -
it's a quantum tachyon manifold.

With a quantum tachyon manifold,
only a single tachyon particle is sent through the manifold.
A tachyon particle takes both the left and right path of each splitter encountered.

Since this is impossible,
the manual recommends the many-worlds interpretation of quantum tachyon splitting:
each time a particle reaches a splitter, it's actually time itself which splits.
In one timeline, the particle went left,
and in the other timeline, the particle went right.

To fix the manifold, what you really need to know is the number of timelines active
after a single particle completes all of its possible journeys through the manifold.

In the above example, there are many timelines.
For instance, there's the timeline where the particle always went left:

.......S.......
.......|.......
......|^.......
......|........
.....|^.^......
.....|.........
....|^.^.^.....
....|..........
...|^.^...^....
...|...........
..|^.^...^.^...
..|............
.|^...^.....^..
.|.............
|^.^.^.^.^...^.
|..............

Or, there's the timeline
where the particle alternated going left and right at each splitter:

.......S.......
.......|.......
......|^.......
......|........
......^|^......
.......|.......
.....^|^.^.....
......|........
....^.^|..^....
.......|.......
...^.^.|.^.^...
.......|.......
..^...^|....^..
.......|.......
.^.^.^|^.^...^.
......|........

Or, there's the timeline
where the particle ends up at the same point as the alternating timeline,
but takes a totally different path to get there:

.......S.......
.......|.......
......|^.......
......|........
.....|^.^......
.....|.........
....|^.^.^.....
....|..........
....^|^...^....
.....|.........
...^.^|..^.^...
......|........
..^..|^.....^..
.....|.........
.^.^.^|^.^...^.
......|........

In this example, in total, the particle ends up on 40 different timelines.

Apply the many-worlds interpretation of quantum tachyon splitting
to your manifold diagram.
In total, how many different timelines would a single tachyon particle end up on?
"""

from enum import StrEnum
from textwrap import dedent
from typing import NamedTuple

type Field = list[list[Cell]]
type Cache = dict[Pos, int]


class Cell(StrEnum):
    START = "S"
    SPACE = "."
    SPLIT = "^"


class Pos(NamedTuple):
    x: int
    y: int


def count_timelines(field: Field) -> int:
    start = _find_start(field)
    return _count_timelines_for_pos(field, start, {})


def _count_timelines_for_pos(field: Field, pos: Pos, cache: Cache) -> int:
    below = Pos(pos.x + 1, pos.y)

    if _is_split(field, below):
        if below not in cache:
            left, right = Pos(pos.x + 2, pos.y - 1), Pos(pos.x + 2, pos.y + 1)
            cache[left] = _count_timelines_for_pos(field, left, cache)
            cache[right] = _count_timelines_for_pos(field, right, cache)
            cache[below] = cache[left] + cache[right]

        return cache[below]

    if _is_space(field, below):
        return _count_timelines_for_pos(field, below, cache)

    return 1


def _find_start(field: Field) -> Pos:
    for x, row in enumerate(field):
        for y, col in enumerate(row):
            if col == Cell.START:
                return Pos(x, y)
    raise ValueError


def _is_split(field: Field, pos: Pos) -> bool:
    try:
        return field[pos.x][pos.y] == Cell.SPLIT
    except IndexError:
        return False


def _is_space(field: Field, pos: Pos) -> bool:
    try:
        return field[pos.x][pos.y] == Cell.SPACE
    except IndexError:
        return False


def _to_array(s: str) -> Field:
    return [list(map(Cell, line)) for line in dedent(s).strip().splitlines()]


field = _to_array(
    """
    .S.
    .^.
    ...
    """,
)
assert count_timelines(field) == 2

field = _to_array(
    """
    ..S..
    .....
    ..^..
    .....
    .^.^.
    .....
    """,
)
assert count_timelines(field) == 4


field = _to_array(
    """
    .......S.......
    ...............
    .......^.......
    ...............
    ......^.^......
    ...............
    .....^.^.^.....
    ...............
    ....^.^...^....
    ...............
    ...^.^...^.^...
    ...............
    ..^...^.....^..
    ...............
    .^.^.^.^.^...^.
    ...............
    """,
)
assert count_timelines(field) == 40


with open("2025/07_laboratories/input.txt") as f:
    print(count_timelines(_to_array(f.read())))
