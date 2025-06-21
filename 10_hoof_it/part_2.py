"""
The reindeer spends a few minutes reviewing your hiking trail map
before realizing something, disappearing for a few minutes,
and finally returning with yet another slightly-charred piece of paper.

The paper describes a second way to measure a trailhead called its rating.
A trailhead's rating is the number of distinct hiking trails
which begin at that trailhead. For example:

.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....

The above map has a single trailhead;
its rating is 3 because there are exactly three distinct hiking trails
which begin at that position:

.....0.   .....0.   .....0.
..4321.   .....1.   .....1.
..5....   .....2.   .....2.
..6....   ..6543.   .....3.
..7....   ..7....   .....4.
..8....   ..8....   ..8765.
..9....   ..9....   ..9....

Here is a map containing a single trailhead with rating 13:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....

This map contains a single trailhead with rating 227
(because there are 121 distinct hiking trails that lead to the 9 on the right edge
and 106 that lead to the 9 on the bottom edge):

012345
123456
234567
345678
4.6789
56789.

Here's the larger example from before:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732

Considering its trailheads in reading order,
they have ratings of 20, 24, 10, 4, 1, 4, 5, 8, and 5.
The sum of all trailhead ratings in this larger example topographic map is 81.

You're not sure how, but the reindeer seems to have crafted
some tiny flags out of toothpicks and bits of paper
and is using them to mark trailheads on your topographic map.
What is the sum of the ratings of all trailheads?
"""

from collections import deque
from collections.abc import Iterable
from textwrap import dedent
from typing import NamedTuple

type TopoMap = list[str]


class Coordinate(NamedTuple):
    x: int
    y: int


class Point(NamedTuple):
    coord: Coordinate
    value: int
    moves: list["Point"]


def get_sum_rating(topo_map: TopoMap) -> int:
    res = 0

    for i, row in enumerate(topo_map):
        for j, c in enumerate(row):
            if c == "0":
                res += _get_trailhead_rating(topo_map, Coordinate(i, j))

    return res


def _get_trailhead_rating(topo_map: TopoMap, coord: Coordinate) -> int:
    p = Point(coord=coord, value=0, moves=[])
    tracker = deque([p])
    res = []

    while tracker:
        p = tracker.pop()

        if p.value == 9:
            res.append(p.coord)
            # _draw_moves(topo_map, p)
            continue

        tracker.extend(_get_next_moves(topo_map, p))

    return len(res)


def _get_next_moves(topo_map: TopoMap, p: Point) -> list[Point]:
    return [qp for qp in _get_quadrant_points(topo_map, p) if qp.value == p.value + 1]


def _get_quadrant_points(topo_map: TopoMap, p: Point) -> Iterable[Point]:
    if p.coord.x - 1 >= 0:
        yield _build_point(topo_map, p.coord.x - 1, p.coord.y, p)  # top

    if p.coord.x + 1 < len(topo_map):
        yield _build_point(topo_map, p.coord.x + 1, p.coord.y, p)  # bottom

    if p.coord.y - 1 >= 0:
        yield _build_point(topo_map, p.coord.x, p.coord.y - 1, p)  # left

    if p.coord.y + 1 < len(topo_map[p.coord.x]):
        yield _build_point(topo_map, p.coord.x, p.coord.y + 1, p)  # right


def _build_point(topo_map: TopoMap, x: int, y: int, previous_point: Point) -> Point:
    try:
        value = int(topo_map[x][y])
    except ValueError:
        value = -1  # for "." placeholders in map

    return Point(
        coord=Coordinate(x, y),
        value=value,
        moves=[*previous_point.moves, previous_point],
    )


def _to_array(s: str) -> list[str]:
    return dedent(s).strip().splitlines()


def _draw_moves(topo_map, p: Point):
    moves = {move.coord for move in p.moves} | {p.coord}

    for i in range(len(topo_map)):
        for j in range(len(topo_map[i])):
            if (i, j) in moves:
                print(topo_map[i][j], end="")
            else:
                print(".", end="")
        print()
    print()


s = _to_array(
    """
    .....0.
    ..4321.
    ..5..2.
    ..6543.
    ..7..4.
    ..8765.
    ..9....
    """,
)
assert get_sum_rating(s) == 3

s = _to_array(
    """
    ..90..9
    ...1.98
    ...2..7
    6543456
    765.987
    876....
    987....
    """,
)
assert get_sum_rating(s) == 13

s = _to_array(
    """
    012345
    123456
    234567
    345678
    4.6789
    56789.
    """,
)
assert get_sum_rating(s) == 227

s = _to_array(
    """
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """,
)
assert get_sum_rating(s) == 81


with open("10_hoof_it/input.txt") as f:
    print(get_sum_rating(_to_array(f.read())))
