"""
The Historians use their fancy device again, this time to whisk you all away
to the North Pole prototype suit manufacturing lab... in the year 1518!
It turns out that having direct access to history
is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important
to avoid anyone from 1518 while The Historians search for the Chief.
Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time
so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^
(to indicate the guard is currently facing up from the perspective of the map).
Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol
which involves repeatedly following these steps:
- If there is something directly in front of you, turn right 90 degrees.
- Otherwise, take a step forward.

Following the above protocol, the guard moves up several times
until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard,
she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers),
she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the mapped area
(after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

By predicting the guard's route,
you can determine which specific positions in the lab will be in the patrol path.
Including the guard's starting position,
the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard.
How many distinct positions will the guard visit before leaving the mapped area?
"""

from enum import StrEnum, auto
from textwrap import dedent


class Direction(StrEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class NoStartError(Exception):
    pass


def mark_routes(map_: list[list[str]]) -> list[str]:
    position = find_start_position(map_)
    direction = Direction.UP

    while True:
        position = go_until_obstacle(position, direction, map_)

        if position is None:
            break

        direction = get_next_direction(direction)

    return map_


def find_start_position(map_: list[list[str]]) -> tuple[int, int]:
    for i in range(len(map_)):
        try:
            j = map_[i].index("^")
        except ValueError:
            continue
        else:
            return (i, j)

    raise NoStartError


def go_until_obstacle(position, direction, map_) -> tuple[int, int] | None:
    i, j = position
    while True:
        map_[i][j] = "X"

        next_i, next_j = get_next_position(i, j, direction)
        if not check_borders(next_i, next_j, map_):
            return None

        if map_[next_i][next_j] == "#":
            return (i, j)

        i, j = next_i, next_j


def check_borders(i, j, map_):
    return 0 <= i < len(map_) and 0 <= j < len(map_[i])


def get_next_position(i, j, direction):
    match direction:
        case Direction.UP:
            return (i - 1, j)
        case Direction.DOWN:
            return (i + 1, j)
        case Direction.LEFT:
            return (i, j - 1)
        case Direction.RIGHT:
            return (i, j + 1)


def get_next_direction(direction: Direction) -> Direction:
    match direction:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP
        case Direction.RIGHT:
            return Direction.DOWN


def count_visits(map_):
    return sum(row.count("X") for row in map_)


def _to_array(s):
    return [list(l) for l in dedent(s).strip().splitlines()]


data = _to_array(
    """
    ^
    """,
)
assert mark_routes(data) == _to_array(
    """
    X
    """,
)

data = _to_array(
    """
    .
    ^
    """,
)
assert mark_routes(data) == _to_array(
    """
    X
    X
    """,
)

data = _to_array(
    """
    #.
    ^.
    """,
)
assert mark_routes(data) == _to_array(
    """
    #.
    XX
    """,
)

data = _to_array(
    """
    #.
    ^#
    ..
    """,
)
assert mark_routes(data) == _to_array(
    """
    #.
    X#
    X.
    """,
)

data = _to_array(
    """
    .#.
    .^#
    .#.
    """,
)
assert mark_routes(data) == _to_array(
    """
    .#.
    XX#
    .#.
    """,
)

data = _to_array(
    """
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
    """,
)
assert (marked := mark_routes(data)) == _to_array(
    """
    ....#.....
    ....XXXXX#
    ....X...X.
    ..#.X...X.
    ..XXXXX#X.
    ..X.X.X.X.
    .#XXXXXXX.
    .XXXXXXX#.
    #XXXXXXX..
    ......#X..
    """,
)
assert count_visits(marked) == 41

with open("2024/06_guard_gallivant/input.txt") as f:
    marked_map = mark_routes(_to_array(f.read()))
