"""
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna.
Much to your surprise, it seems to have been reconfigured to emit a signal
that makes people 0.1% more likely to buy
Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas.
Each antenna is tuned to a specific frequency indicated by
a single lowercase letter, uppercase letter, or digit.
You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............

The signal only applies its nefarious effect at specific antinodes
based on the resonant frequencies of the antennas.
In particular, an antinode occurs at any point
that is perfectly in line with two antennas of the same frequency -
but only when one of the antennas is twice as far away as the other.
This means that for any pair of antennas with the same frequency,
there are two antinodes, one on either side of them.

So, for these two antennas with frequency a,
they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........

Adding a third antenna with the same frequency creates several more antinodes.
It would ideally add four antinodes, but two are off the right side of the map,
so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........

Antennas with different frequencies don't create antinodes;
A and a count as different frequencies.
However, antinodes can occur at locations that contain antennas.
In this diagram, the lone antenna with frequency capital A creates no antinodes
but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........

The first example has antennas with two different frequencies,
so the antinodes they create look like this,
plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.

Because the topmost A-frequency antenna overlaps with a 0-frequency antinode,
there are 14 total unique locations
that contain an antinode within the bounds of the map.

Calculate the impact of the signal.
How many unique locations within the bounds of the map contain an antinode?
"""

from collections import defaultdict
from collections.abc import Iterable
from itertools import combinations
from textwrap import dedent
from typing import NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int


def get_all_antinodes(input: list[str]) -> set[Coordinate]:
    all_coordinates = convert_input_to_coordinates(input)
    antinodes = []

    for coordinates in all_coordinates.values():
        for pair in combinations(coordinates, r=2):
            antinodes.extend(get_antinodes_for_pair(*pair))

    antinodes = drop_out_of_bound_antinodes(
        antinodes,
        max_x=len(input),
        max_y=len(input[0]),
    )
    return deduplicate(antinodes)


def convert_input_to_coordinates(input: list[str]) -> dict[str, list[Coordinate]]:
    coordinates = defaultdict(list)

    for i in range(len(input)):
        for j in range(len(input[i])):
            char = input[i][j]
            if char not in ".#":
                coordinates[char].append(Coordinate(i, j))

    return coordinates


def get_antinodes_for_pair(a: Coordinate, b: Coordinate) -> list[Coordinate]:
    diff_x = a.x - b.x
    diff_y = a.y - b.y
    return [(a.x + diff_x, a.y + diff_y), (b.x - diff_x, b.y - diff_y)]


def drop_out_of_bound_antinodes(
    antinodes: list[Coordinate],
    max_x: int,
    max_y: int,
) -> Iterable[Coordinate]:
    for x, y in antinodes:
        if 0 <= x < max_x and 0 <= y < max_y:
            yield (x, y)


def deduplicate(seq) -> set[Coordinate]:
    return sorted(set(seq))


def _to_array(s: str):
    return dedent(s).strip().splitlines()


s = _to_array(
    """
    aA
    """,
)
assert convert_input_to_coordinates(s) == {"a": [(0, 0)], "A": [(0, 1)]}

s = _to_array(
    """
    #...
    .a..
    ..a.
    ...#
    """,
)
assert get_all_antinodes(s) == [(0, 0), (3, 3)]

s = _to_array(
    """
    ...#
    ..a.
    .a..
    #...
    """,
)
assert get_all_antinodes(s) == [(0, 3), (3, 0)]

s = _to_array(
    """
    .#.
    .a.
    .a.
    .#.
    """,
)
assert get_all_antinodes(s) == [(0, 1), (3, 1)]

s = _to_array(
    """
    #aa#
    """,
)
assert get_all_antinodes(s) == [(0, 0), (0, 3)]

s = _to_array(
    """
    #aa#AA#
    """,
)
assert get_all_antinodes(s) == [(0, 0), (0, 3), (0, 6)]

s = _to_array(
    """
    aAA#
    """,
)
assert get_all_antinodes(s) == [(0, 0), (0, 3)]

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
assert get_all_antinodes(s) == []

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
assert get_all_antinodes(s) == [(0, 0), (0, 3), (1, 0), (1, 3)]

s = _to_array(
    """
    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............
    """,
)
assert get_all_antinodes(s) == [
    (0, 6),
    (0, 11),
    (1, 3),
    (2, 4),
    (2, 10),
    (3, 2),
    (4, 9),
    (5, 1),
    (5, 6),
    (6, 3),
    (7, 0),
    (7, 7),
    (10, 10),
    (11, 10),
]

with open("2024/08_resonant_collinearity/input.txt") as f:
    print(len(get_all_antinodes(_to_array(f.read()))))
