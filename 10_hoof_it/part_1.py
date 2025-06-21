"""
You all arrive at a Lava Production Facility on a floating island in the sky.
As the others begin to search the massive industrial complex,
you feel a small nose boop your leg
and look down to discover a reindeer wearing a hard hat.

The reindeer is holding a book titled "Lava Island Hiking Guide".
However, when you open the book,
you discover that most of it seems to have been scorched by lava!
As you're about to ask how you can help,
the reindeer brings you a blank topographic map of the surrounding area
(your puzzle input) and looks up at you excitedly.

Perhaps you can help fill in the missing hiking trails?

The topographic map indicates the height at each position
using a scale from 0 (lowest) to 9 (highest). For example:

0123
1234
8765
9876

Based on un-scorched scraps of the book,
you determine that a good hiking trail is as long as possible
and has an even, gradual, uphill slope.
For all practical purposes,
this means that a hiking trail is any path that starts at height 0, ends at height 9,
and always increases by a height of exactly 1 at each step.
Hiking trails never include diagonal steps - only up, down, left, or right
(from the perspective of the map).

You look up from the map
and notice that the reindeer has helpfully begun to construct
a small pile of pencils, markers, rulers, compasses, stickers, and other equipment
you might need to update the map with hiking trails.

A trailhead is any position that starts one or more hiking trails -
here, these positions will always have height 0.
Assembling more fragments of pages,
you establish that a trailhead's score
is the number of 9-height positions reachable from that trailhead via a hiking trail.
In the above example, the single trailhead in the top left corner
has a score of 1 because it can reach a single 9 (the one in the bottom left).

This trailhead has a score of 2:

...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9

(The positions marked . are impassable tiles to simplify these examples;
they do not appear on your actual topographic map.)

This trailhead has a score of 4 because every 9 is reachable via a hiking trail
except the one immediately to the left of the trailhead:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....

This topographic map contains two trailheads;
the trailhead at the top has a score of 1,
while the trailhead at the bottom has a score of 2:

10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01

Here's a larger example:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732

This larger example has 9 trailheads.
Considering the trailheads in reading order,
they have scores of 5, 6, 5, 3, 1, 3, 5, 3, and 5.
Adding these scores together, the sum of the scores of all trailheads is 36.

The reindeer gleefully carries over a protractor and adds it to the pile.
What is the sum of the scores of all trailheads on your topographic map?
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


def get_sum_score(topo_map: TopoMap) -> int:
    res = 0

    for i, row in enumerate(topo_map):
        for j, c in enumerate(row):
            if c == "0":
                res += _get_trailhead_score(topo_map, Coordinate(i, j))

    return res


def _get_trailhead_score(topo_map: TopoMap, coord: Coordinate) -> int:
    p = Point(coord=coord, value=0, moves=[])
    tracker = deque([p])
    res = set()

    while tracker:
        p = tracker.pop()

        if p.value == 9:
            res.add(p.coord)
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
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    """,
)
assert get_sum_score(s) == 1

s = _to_array(
    """
    ...0...
    ...1...
    ...2...
    6543456
    7.....7
    8.....8
    9.....9
    """,
)
assert get_sum_score(s) == 2

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
assert get_sum_score(s) == 4

s = _to_array(
    """
    10..9..
    2...8..
    3...7..
    4567654
    ...8..3
    ...9..2
    .....01
    """,
)
assert get_sum_score(s) == 3

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
assert get_sum_score(s) == 36

with open("10_hoof_it/input.txt") as f:
    print(get_sum_score(_to_array(f.read())))
