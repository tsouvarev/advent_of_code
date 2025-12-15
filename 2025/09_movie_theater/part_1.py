"""
You slide down the firepole in the corner of the playground
and land in the North Pole base movie theater!

The movie theater has a big tile floor with an interesting pattern.
Elves here are redecorating the theater
by switching out some of the square tiles in the big grid they form.
Some of the tiles are red; the Elves would like to find the largest rectangle
that uses red tiles for two of its opposite corners.
They even have a list of where the red tiles are located in the grid.

For example:

7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3

Showing red tiles as # and other tiles as .,
the above arrangement of red tiles would look like this:

..............
.......#...#..
..............
..#....#......
..............
..#......#....
..............
.........#.#..
..............

You can choose any two red tiles as the opposite corners of your rectangle;
your goal is to find the largest rectangle possible.

For example, you could make a rectangle (shown as O)
with an area of 24 between 2,5 and 9,7:

..............
.......#...#..
..............
..#....#......
..............
..OOOOOOOO....
..OOOOOOOO....
..OOOOOOOO.#..
..............

Or, you could make a rectangle with area 35 between 7,1 and 11,7:

..............
.......OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
.......OOOOO..
..............

You could even make a thin rectangle with an area of only 6 between 7,3 and 2,3:

..............
.......#...#..
..............
..OOOOOO......
..............
..#......#....
..............
.........#.#..
..............

Ultimately, the largest rectangle you can make in this example has area 50.
One way to do this is between 2,5 and 11,1:

..............
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..............
.........#.#..
..............

Using two red tiles as opposite corners,
what is the largest area of any rectangle you can make?
"""

from itertools import combinations
from typing import NamedTuple


class Tile(NamedTuple):
    x: int
    y: int


def find_biggest_rectangle(tiles: list[Tile]):
    max_area = 0

    for comb in combinations(tiles, 2):
        max_area = max(max_area, _get_area(*comb))

    return max_area


def _get_area(tile_1: Tile, tile_2: Tile) -> int:
    dx = abs(tile_1.x - tile_2.x) + 1
    dy = abs(tile_1.y - tile_2.y) + 1
    return dx * dy


def _parse_tile(raw_tile: str) -> Tile:
    return Tile(*map(int, raw_tile.split(",")))


assert _get_area(Tile(2, 5), Tile(9, 7)) == 24
assert _get_area(Tile(7, 1), Tile(11, 7)) == 35
assert _get_area(Tile(7, 3), Tile(2, 3)) == 6
assert _get_area(Tile(2, 5), Tile(11, 1)) == 50

tiles = [
    Tile(7, 1),
    Tile(11, 1),
    Tile(11, 7),
    Tile(9, 7),
    Tile(9, 5),
    Tile(2, 5),
    Tile(2, 3),
    Tile(7, 3),
]
assert find_biggest_rectangle(tiles) == 50


with open("2025/09_movie_theater/input.txt") as f:
    tiles = [_parse_tile(line.strip()) for line in f]
    print(find_biggest_rectangle(tiles))
