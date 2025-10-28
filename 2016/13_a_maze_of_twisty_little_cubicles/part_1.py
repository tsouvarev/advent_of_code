"""
You arrive at the first floor of this new building
to discover a much less welcoming environment than the shiny atrium of the last one.
Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative integers (x,y).
Each such coordinate is either a wall or an open space. You can't move diagonally.
The cube maze starts at 0,0 and seems to extend infinitely toward positive x and y;
negative values are invalid, as they represent a location outside the building.
You are in a small waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains,
the layout is actually quite logical.
You can determine whether a given x,y coordinate will be a wall
or an open space using a simple system:

- Find x*x + 3*x + 2*x*y + y + y*y.
- Add the office designer's favorite number (your puzzle input).
- Find the binary representation of that sum; count the number of bits that are 1.
  - If the number of bits that are 1 is even, it's an open space.
  - If the number of bits that are 1 is odd, it's a wall.

For example, if the office designer's favorite number were 10,
drawing walls as # and open spaces as .,
the corner of the building containing 0,0 would look like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###

Now, suppose you wanted to reach 7,4. The shortest route you could take is marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###

Thus, reaching 7,4 would take a minimum of 11 steps
(starting from your current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?
"""

from collections import deque
from collections.abc import Iterator
from functools import cache
from math import inf

type Coord = tuple[int, int]
type Trace = list[Coord]


def walk_maze(seed: int, x: int, y: int) -> Trace:
    traces = deque([[(1, 1)]])
    min_trace = []
    min_trace_len = inf

    while traces:
        trace = traces.popleft()
        _x, _y = trace[-1]

        if (_x, _y) == (x, y) and len(trace) < min_trace_len:
            min_trace = trace
            min_trace_len = len(trace)

        if len(trace) > min_trace_len:
            continue

        for step in _get_next_steps(seed, _x, _y):
            if step not in trace:
                traces.append([*trace, step])

    return min_trace


def _get_next_steps(seed: int, x: int, y: int) -> Iterator[Coord]:
    if y - 1 >= 0 and _is_space(seed, x, y - 1):
        yield (x, y - 1)

    if _is_space(seed, x + 1, y):
        yield (x + 1, y)

    if _is_space(seed, x, y + 1):
        yield (x, y + 1)

    if x - 1 >= 0 and _is_space(seed, x - 1, y):
        yield (x - 1, y)


@cache
def _is_space(seed: int, x: int, y: int) -> bool:
    value = seed + x * x + 3 * x + 2 * x * y + y + y * y
    return value.bit_count() % 2 == 0


def _print_trace(seed: int, trace: Trace) -> None:
    max_x, max_y = map(max, zip(*trace))

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in trace:
                print("0", end="")
            elif _is_space(seed, x, y):
                print(".", end="")
            else:
                print("#", end="")
        print()


assert _is_space(10, 1, 1) is True
assert _is_space(10, 2, 1) is False

assert walk_maze(10, 1, 2) == [(1, 1), (1, 2)]
assert walk_maze(10, 2, 2) == [(1, 1), (1, 2), (2, 2)]
assert walk_maze(10, 3, 3) == [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]
assert walk_maze(10, 7, 4) == [
    (1, 1),
    (1, 2),
    (2, 2),
    (3, 2),
    (3, 3),
    (3, 4),
    (4, 4),
    (4, 5),
    (5, 5),
    (6, 5),
    (6, 4),
    (7, 4),
]

print(len(walk_maze(1364, 31, 39)))
