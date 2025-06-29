"""
Watching over your shoulder as you work, one of The Historians asks
if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out
that an antinode occurs at any grid position
exactly in line with at least two antennas of the same frequency,
regardless of distance.
This means that some of the new antinodes will occur at the position
of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........

In fact, the three T-frequency antennas are all exactly in line with two antennas,
so they are all also antinodes!
This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes,
including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##

Calculate the impact of the signal using this updated model.
How many unique locations within the bounds of the map contain an antinode?
"""

from collections import defaultdict
from collections.abc import Iterable
from itertools import combinations, count
from textwrap import dedent
from typing import NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int


def get_all_antinodes(input: list[str]) -> set[Coordinate]:
    all_coordinates = _convert_input_to_coordinates(input)
    antinode_generators = []

    for coordinates in all_coordinates.values():
        for pair in combinations(coordinates, r=2):
            antinode_generators.extend(_get_antinodes_for_pair(*pair))

    antinodes = drop_out_of_bound_coordinates(
        antinode_generators,
        max_x=len(input),
        max_y=len(input[0]),
    )

    return _deduplicate(antinodes)


def _convert_input_to_coordinates(input: list[str]) -> dict[str, list[Coordinate]]:
    coordinates = defaultdict(list)

    for i in range(len(input)):
        for j in range(len(input[i])):
            char = input[i][j]
            if char not in ".#":
                coordinates[char].append(Coordinate(i, j))

    return coordinates


def _get_antinodes_for_pair(
    a: Coordinate,
    b: Coordinate,
) -> tuple[Iterable[Coordinate]]:
    diff_x = a.x - b.x
    diff_y = a.y - b.y

    return _build_antinodes(a, diff_x, diff_y), _build_antinodes(b, -diff_x, -diff_y)


def _build_antinodes(p: Coordinate, diff_x: int, diff_y: int) -> Iterable[Coordinate]:
    yield p

    for k in count(1):
        yield Coordinate(p.x + k * diff_x, p.y + k * diff_y)


def drop_out_of_bound_coordinates(
    antinode_generators: list[Iterable[Coordinate]],
    max_x: int,
    max_y: int,
) -> Iterable[Coordinate]:
    for gen in antinode_generators:
        for p in gen:
            if 0 <= p.x < max_x and 0 <= p.y < max_y:
                yield p
            else:
                break


def _deduplicate(seq) -> list[Coordinate]:
    return sorted(set(seq))


def _to_array(s: str):
    return dedent(s).strip().splitlines()


s = _to_array(
    """
    aA
    """,
)
assert _convert_input_to_coordinates(s) == {"a": [(0, 0)], "A": [(0, 1)]}

s = _to_array(
    """
    #...
    .a..
    ..a.
    ...#
    """,
)
assert get_all_antinodes(s) == [(0, 0), (1, 1), (2, 2), (3, 3)]

s = _to_array(
    """
    ...#
    ..a.
    .a..
    #...
    """,
)
assert get_all_antinodes(s) == [(0, 3), (1, 2), (2, 1), (3, 0)]

s = _to_array(
    """
    .#.
    .a.
    .a.
    .#.
    """,
)
assert get_all_antinodes(s) == [(0, 1), (1, 1), (2, 1), (3, 1)]

s = _to_array(
    """
    #aa#
    """,
)
assert get_all_antinodes(s) == [(0, 0), (0, 1), (0, 2), (0, 3)]

s = _to_array(
    """
    #aa#AA#
    """,
)
assert get_all_antinodes(s) == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]

s = _to_array(
    """
    aAA#
    """,
)
assert get_all_antinodes(s) == [(0, 0), (0, 1), (0, 2), (0, 3)]

s = _to_array(
    """
    a
    """,
)
assert get_all_antinodes(s) == []

s = _to_array(
    """
    .a.a.
    """,
)
assert get_all_antinodes(s) == [(0, 1), (0, 3)]

s = _to_array(
    """
    .#.#.a.a.#.
    """,
)
assert get_all_antinodes(s) == [(0, 1), (0, 3), (0, 5), (0, 7), (0, 9)]

s = _to_array(
    """
    .a.A.
    """,
)
assert get_all_antinodes(s) == []

s = _to_array(
    """
    #aa#
    #AA#
    """,
)
assert get_all_antinodes(s) == [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 0),
    (1, 1),
    (1, 2),
    (1, 3),
]

s = _to_array(
    """
    ##....#....#
    .#.#....0...
    ..#.#0....#.
    ..##...0....
    ....0....#..
    .#...#A....#
    ...#..#.....
    #....#.#....
    ..#.....A...
    ....#....A..
    .#........#.
    ...#......##
    """,
)
assert get_all_antinodes(s) == [
    (0, 0),
    (0, 1),
    (0, 6),
    (0, 11),
    (1, 1),
    (1, 3),
    (1, 8),
    (2, 2),
    (2, 4),
    (2, 5),
    (2, 10),
    (3, 2),
    (3, 3),
    (3, 7),
    (4, 4),
    (4, 9),
    (5, 1),
    (5, 5),
    (5, 6),
    (5, 11),
    (6, 3),
    (6, 6),
    (7, 0),
    (7, 5),
    (7, 7),
    (8, 2),
    (8, 8),
    (9, 4),
    (9, 9),
    (10, 1),
    (10, 10),
    (11, 3),
    (11, 10),
    (11, 11),
]

with open("2024/08_resonant_collinearity/input.txt") as f:
    print(len(get_all_antinodes(_to_array(f.read()))))
