"""
You've finally met your match;
the doors that provide access to the roof are locked tight,
and all of the controls and related electronics are inaccessible.
You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot,
but you reconfigure it to be able to interface with some of the exposed wires
that have been routed through the HVAC system.
If you can direct it to each of those locations,
you should be able to bypass the security controls.

You extract the duct layout for this area from some blueprints you acquired
and create a map with the relevant locations marked (your puzzle input).
0 is your current location, from which the cleaning robot embarks;
the other numbers are (in no particular order) the locations
the robot needs to visit at least once each.
Walls are marked as #, and open passages are marked as ..
Numbers behave like open passages.

For example, suppose you have a map like the following:

###########
#0.1.....2#
#.#######.#
#4.......3#
###########

To reach all of the points of interest as quickly as possible,
you would have the robot take the following path:

- 0 to 4 (2 steps)
- 4 to 1 (4 steps; it can't move diagonally)
- 1 to 2 (6 steps)
- 2 to 3 (2 steps)

Since the robot isn't very fast, you need to find it the shortest route.
This path is the fewest steps (in the above example, a total of 14)
required to start at 0 and then visit every other location at least once.

Given your actual map, and starting from location 0,
what is the fewest number of steps
required to visit every non-0 number marked on the map at least once?
"""

from collections import deque
from collections.abc import Iterator
from itertools import pairwise, permutations
from math import inf
from typing import NamedTuple


class Stop(NamedTuple):
    n: int
    coord: Coord


class Coord(NamedTuple):
    x: int
    y: int


type Field = list[list[str]]
type Route = list[Coord]
WALL, PASS = "#", "."


def solve(field: Field, *, ends_at_zero: bool = False) -> tuple[int, list[int]]:
    zero, *stops = _find_stops(field)

    min_path = int(inf)
    min_combo = ()
    distances = {}

    for _i, combo in enumerate(permutations(stops, len(stops))):
        path_len = 0
        full_combo = [zero, *combo]
        if ends_at_zero:
            full_combo.append(zero)

        for pair in pairwise(full_combo):
            if pair not in distances:
                start, end = pair
                route = _build_route(field, start.coord, end.coord)
                distances[(start, end)] = distances[(end, start)] = len(route)

            path_len += distances[pair]

        if min_path > path_len:
            min_path = path_len
            min_combo = full_combo

    return min_path, [s.n for s in min_combo]


def _find_stops(field: Field) -> list[Stop]:
    res = []
    for y, row in enumerate(field):
        for x, col in enumerate(row):
            if col.isnumeric():
                res.append(Stop(n=int(col), coord=Coord(x, y)))
    return sorted(res)


def _build_route(field: Field, start: Coord, end: Coord) -> Route:
    queue = deque([[start]])
    visited = set()

    while queue:
        *curr_path, curr_node = queue.popleft()

        next_steps = _get_next_steps(field, curr_node, end)
        for step in next_steps:
            path = [*curr_path, curr_node, step]

            if step == end:
                return path[1:]  # exclude start

            if step not in visited:
                queue.append(path)
                visited.add(step)

    raise ValueError


def _get_next_steps(field: Field, c: Coord, end: Coord) -> Iterator[Coord]:
    if c.y > 0 and _is_passable(field[c.y - 1][c.x]):
        yield Coord(c.x, c.y - 1)

    if c.x > 0 and _is_passable(field[c.y][c.x - 1]):
        yield Coord(c.x - 1, c.y)

    if c.y + 1 < len(field) and _is_passable(field[c.y + 1][c.x]):
        yield Coord(c.x, c.y + 1)

    if c.x + 1 < len(field[c.y]) and _is_passable(field[c.y][c.x + 1]):
        yield Coord(c.x + 1, c.y)


def _is_passable(c: str) -> bool:
    return c == PASS or c.isnumeric()


def _to_field(*rows: str) -> Field:
    return [list(row) for row in rows]


field = _to_field(
    "1.3",
    "2.0",
)
assert _find_stops(field) == [(0, (2, 1)), (1, (0, 0)), (2, (0, 1)), (3, (2, 0))]

field = _to_field(
    "...",
    "...",
    "...",
)
assert set(_get_next_steps(field, Coord(1, 1), Coord(1, 1))) == {
    Coord(1, 0),
    Coord(2, 1),
    Coord(1, 2),
    Coord(0, 1),
}


field = _to_field(
    ".#.",
    "...",
    "...",
)
assert set(_get_next_steps(field, Coord(1, 1), Coord(1, 1))) == {
    Coord(2, 1),
    Coord(1, 2),
    Coord(0, 1),
}


field = _to_field(
    "...",
    "..#",
    "...",
)
assert set(_get_next_steps(field, Coord(1, 1), Coord(1, 1))) == {
    Coord(1, 0),
    Coord(1, 2),
    Coord(0, 1),
}


field = _to_field(
    "...",
    "...",
    ".#.",
)
assert set(_get_next_steps(field, Coord(1, 1), Coord(1, 1))) == {
    Coord(1, 0),
    Coord(2, 1),
    Coord(0, 1),
}


field = _to_field(
    "...",
    "#..",
    "...",
)
assert set(_get_next_steps(field, Coord(1, 1), Coord(1, 1))) == {
    Coord(1, 0),
    Coord(2, 1),
    Coord(1, 2),
}


field = _to_field(".")
assert set(_get_next_steps(field, Coord(0, 0), Coord(1, 1))) == set()


field = _to_field(
    "..",
    "..",
)
assert _build_route(field, Coord(0, 0), Coord(1, 1)) == [
    Coord(0, 1),
    Coord(1, 1),
]

field = _to_field(
    "...",
    "#.#",
    "...",
)
assert _build_route(field, Coord(0, 0), Coord(2, 2)) == [
    Coord(1, 0),
    Coord(1, 1),
    Coord(1, 2),
    Coord(2, 2),
]

field = _to_field(
    "....",
    "#.#.",
    "....",
)
assert _build_route(field, Coord(0, 0), Coord(2, 2)) == [
    Coord(1, 0),
    Coord(1, 1),
    Coord(1, 2),
    Coord(2, 2),
]

field = _to_field(
    "###########",
    "#0.1.....2#",
    "#.#######.#",
    "#4.......3#",
    "###########",
)
assert solve(field) == (14, [0, 4, 1, 2, 3])


with open("2016/24_air_duct_spelunking/input.txt") as f:
    field = _to_field(*[line.strip() for line in f])
    print(solve(field))
    print(solve(field, ends_at_zero=True))
