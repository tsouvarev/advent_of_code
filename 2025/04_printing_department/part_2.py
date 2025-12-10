"""
Now, the Elves just need help accessing as much of the paper as they can.

Once a roll of paper can be accessed by a forklift, it can be removed.
Once a roll of paper is removed, the forklifts might be able
to access more rolls of paper, which they might also be able to remove.
How many total rolls of paper could the Elves remove
if they keep repeating this process?

Starting with the same example as above,
here is one way you could remove as many rolls of paper as possible,
using highlighted @ to indicate that a roll of paper is about to be removed,
and using x to indicate that a roll of paper was just removed:

Initial state:
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

Remove 13 rolls of paper:
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

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Stop once no more rolls of paper are accessible by a forklift.
In this example, a total of 43 rolls of paper can be removed.

Start with your original diagram.
How many rolls of paper in total can be removed by the Elves and their forklifts?
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


def run_forklifts(maze: Maze) -> list[Point]:
    res = []

    while True:
        papers_to_remove = _get_accessible_points(maze)

        if papers_to_remove:
            res.extend(papers_to_remove)
        else:
            break

        maze = _remove_papers(maze, papers_to_remove)

    return res


def _get_accessible_points(maze: Maze) -> list[Point]:
    res = []

    for i, row in enumerate(maze):
        for j, _ in enumerate(row):
            p = Point(i, j)
            papers_around = (_is_paper(maze, n) for n in _get_neighbors(p))

            if _is_paper(maze, p) and sum(papers_around) < 4:
                res.append(p)

    return res


def _remove_papers(maze: Maze, points: list[Point]) -> Maze:
    for p in points:
        maze[p.x][p.y] = Cell.FREE
    return maze


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
assert _get_accessible_points(maze) == []

maze = _to_maze(
    """
    @
    """,
)
assert _get_accessible_points(maze) == [(0, 0)]

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
assert _get_accessible_points(maze) == [
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
assert len(run_forklifts(maze)) == 43


with open("2025/04_printing_department/input.txt") as f:
    print(len(run_forklifts(_to_maze(f.read()))))
