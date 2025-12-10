"""
You ride the escalator down to the printing department.
They're clearly getting ready for Christmas;
they have lots of large rolls of paper everywhere,
and there's even a massive printer in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations.
What you really need is a way to get further into the North Pole base
while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help.
"We're pretty sure there's a cafeteria on the other side of the back wall.
If we could break through the wall, you'd be able to keep moving.
It's too bad all of our forklifts are so busy moving those big rolls of paper around."

If you can optimize the work the forklifts are doing,
maybe they would have time to spare to break through the wall.

The rolls of paper (@) are arranged on a large grid;
the Elves even have a helpful diagram (your puzzle input)
indicating where everything is located.

For example:

..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

The forklifts can only access a roll of paper
if there are fewer than four rolls of paper in the eight adjacent positions.
If you can figure out which rolls of paper the forklifts can access,
they'll spend less time looking and more time breaking down the wall to the cafeteria.

In this example, there are 13 rolls of paper that can be accessed by a forklift
(marked with x):

..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Consider your complete diagram of the paper roll locations.
How many rolls of paper can be accessed by a forklift?
"""

from collections.abc import Iterable
from enum import StrEnum
from textwrap import dedent
from typing import NamedTuple

type Maze = list[list[Cell]]


class Point(NamedTuple):
    x: int
    y: int


class Cell(StrEnum):
    FREE = "."
    PAPER = "@"


def get_accessible_points(maze: Maze) -> list[Point]:
    res = []

    for i, row in enumerate(maze):
        for j, _ in enumerate(row):
            p = Point(i, j)
            papers_around = (_is_paper(maze, n) for n in _get_neighbors(p))

            if _is_paper(maze, p) and sum(papers_around) < 4:
                res.append(p)

    return res


def _get_neighbors(p: Point) -> Iterable[Point]:
    yield Point(p.x - 1, p.y - 1)
    yield Point(p.x - 1, p.y)
    yield Point(p.x - 1, p.y + 1)

    yield Point(p.x, p.y - 1)
    yield Point(p.x, p.y + 1)

    yield Point(p.x + 1, p.y - 1)
    yield Point(p.x + 1, p.y)
    yield Point(p.x + 1, p.y + 1)


def _is_paper(maze: Maze, p: Point) -> bool:
    if 0 <= p.x < len(maze) and 0 <= p.y < len(maze[p.x]):
        return maze[p.x][p.y] == Cell.PAPER

    return False


def _to_maze(s: str) -> Maze:
    return [[Cell(c) for c in line] for line in dedent(s).strip().splitlines()]


maze = _to_maze(
    """
    .
    """,
)
assert get_accessible_points(maze) == []

maze = _to_maze(
    """
    @
    """,
)
assert get_accessible_points(maze) == [(0, 0)]


maze = _to_maze(
    """
    ..@@.@@@@.
    @@@.@.@.@@
    @@@@@.@.@@
    @.@@@@..@.
    @@.@@@@.@@
    .@@@@@@@.@
    .@.@.@.@@@
    @.@@@.@@@@
    .@@@@@@@@.
    @.@.@@@.@.
    """,
)
assert get_accessible_points(maze) == [
    (0, 2),
    (0, 3),
    (0, 5),
    (0, 6),
    (0, 8),
    (1, 0),
    (2, 6),
    (4, 0),
    (4, 9),
    (7, 0),
    (9, 0),
    (9, 2),
    (9, 8),
]


with open("2025/04_printing_department/input.txt") as f:
    print(len(get_accessible_points(_to_maze(f.read()))))
