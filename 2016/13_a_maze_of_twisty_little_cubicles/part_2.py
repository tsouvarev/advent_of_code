"""
How many locations (distinct x,y coordinates, including your starting location)
can you reach in at most 50 steps?
"""

from collections import deque
from collections.abc import Iterator
from functools import cache
from typing import NamedTuple

type Trace = list[Coord]


class Coord(NamedTuple):
    x: int
    y: int


class Frontier(NamedTuple):
    coord: Coord
    steps: int


def walk_maze(seed: int, max_steps: int) -> set[Coord]:
    frontiers = deque([Frontier(Coord(1, 1), 0)])
    visited = set()

    while frontiers:
        f = frontiers.popleft()
        visited.add(f.coord)

        if f.steps == max_steps:
            continue

        for step in _get_next_steps(f.coord):
            if _is_space(seed, step) and step not in visited:
                frontiers.append(Frontier(step, f.steps + 1))

    return visited


def _get_next_steps(c: Coord) -> Iterator[Coord]:
    if c.y - 1 >= 0:
        yield Coord(c.x, c.y - 1)

    yield Coord(c.x + 1, c.y)
    yield Coord(c.x, c.y + 1)

    if c.x - 1 >= 0:
        yield Coord(c.x - 1, c.y)


@cache
def _is_space(seed: int, c: Coord) -> bool:
    value = seed + c.x**2 + 3 * c.x + 2 * c.x * c.y + c.y + c.y**2
    return value.bit_count() % 2 == 0


assert _is_space(10, Coord(1, 1)) is True
assert _is_space(10, Coord(2, 1)) is False

assert walk_maze(10, 1) == {(1, 1), (0, 1), (1, 2)}
assert walk_maze(10, 2) == {(1, 1), (0, 1), (1, 2), (0, 0), (2, 2)}

print(len(walk_maze(1364, 50)))
