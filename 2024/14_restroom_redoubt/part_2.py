"""
During the bathroom break, someone notices that
these robots seem awfully similar to ones built and used at the North Pole.
If they're the same type of robots, they should have a hard-coded Easter egg:
very rarely, most of the robots should arrange themselves
into a picture of a Christmas tree.

What is the fewest number of seconds that must elapse
for the robots to display the Easter egg?
"""

import re
from collections import Counter, defaultdict
from collections.abc import Iterable
from functools import reduce
from itertools import count, starmap
from operator import mul
from typing import NamedTuple


class Robot(NamedTuple):
    start: Coordinate
    moves: Move


class Coordinate(NamedTuple):
    x: int
    y: int


class Move(NamedTuple):
    x: int
    y: int


class Map(NamedTuple):
    x: int
    y: int


class Quadrant(NamedTuple):
    from_: Coordinate
    to_: Coordinate


def move_robots(robots: list[Robot], tile_map: Map, seconds: int) -> list[Coordinate]:
    return sorted(move_robot(robot, tile_map, seconds) for robot in robots)


def move_robot(robot: Robot, tile_map: Map, seconds: int) -> Coordinate:
    shifted = (
        robot.start.x + robot.moves.x * seconds,
        robot.start.y + robot.moves.y * seconds,
    )
    return Coordinate(shifted[0] % tile_map.x, shifted[1] % tile_map.y)


def find_safety_factor(positions: list[Coordinate], tile_map: Map) -> int:
    quadrants = _get_quadrants(tile_map)
    safety_by_quadrants = defaultdict(int)

    for p in positions:
        for i, q in enumerate(quadrants):
            if q.from_.x <= p.x < q.to_.x and q.from_.y <= p.y < q.to_.y:
                safety_by_quadrants[i] += 1

    return reduce(mul, safety_by_quadrants.values(), 1)


def _get_quadrants(tile_map: Map):
    skip_x, skip_y = tile_map.x % 2, tile_map.y % 2
    half_x, half_y = tile_map.x // 2, tile_map.y // 2
    return [
        # top left
        Quadrant(from_=Coordinate(0, 0), to_=Coordinate(half_x, half_y)),
        # top right
        Quadrant(
            from_=Coordinate(half_x + skip_x, 0),
            to_=Coordinate(tile_map.x, half_y),
        ),
        # bottom left
        Quadrant(
            from_=Coordinate(0, half_y + skip_y),
            to_=Coordinate(half_x, tile_map.y),
        ),
        # bottom right
        Quadrant(
            from_=Coordinate(half_x + skip_x, half_y + skip_y),
            to_=Coordinate(tile_map.x, tile_map.y),
        ),
    ]


def _gen_move_robot(start, moves, tile_map):
    for i in count(1):
        yield move_robot(_gen_robot(start, moves), Map(*tile_map), seconds=i)


def _gen_move_robots(robots, tile_map):
    for i in count(1):
        yield move_robots(robots, Map(*tile_map), seconds=i)


def _gen_robot(start, moves):
    return Robot(Coordinate(*start), Move(*moves))


def _draw_positions(positions: list[Coordinate], tile_map: Map):
    robot_positions = Counter(positions)
    for j in range(tile_map.y):
        for i in range(tile_map.x):
            print(robot_positions[(i, j)] or ".", end="")
        print()


def _draw_robots(robots: list[Robot], tile_map: Map):
    robot_positions = Counter(r.start for r in robots)
    for j in range(tile_map.y):
        for i in range(tile_map.x):
            print(robot_positions[(i, j)] or ".", end="")
        print()


def _find_xmas_tree(positions_generator: Iterable[Coordinate], tile_map: Map) -> bool:
    lowest_safety_factor = find_safety_factor(next(positions_generator), tile_map)

    for i, positions in enumerate(positions_generator, 2):
        safety_factor = find_safety_factor(positions, tile_map)
        if safety_factor < lowest_safety_factor:
            lowest_safety_factor = safety_factor
            print(i)
            yield positions


robot = _gen_move_robot((2, 4), (2, -3), (11, 7))

assert next(robot) == (4, 1)
assert next(robot) == (6, 5)
assert next(robot) == (8, 2)
assert next(robot) == (10, 6)
assert next(robot) == (1, 3)

robots = list(
    starmap(
        _gen_robot,
        [
            [(0, 4), (3, -3)],
            [(6, 3), (-1, -3)],
            [(10, 3), (-1, 2)],
            [(2, 0), (2, -1)],
            [(0, 0), (1, 3)],
            [(3, 0), (-2, -2)],
            [(7, 6), (-1, -3)],
            [(3, 0), (-1, -2)],
            [(9, 3), (2, 3)],
            [(7, 3), (-1, 2)],
            [(2, 4), (2, -3)],
            [(9, 5), (-3, -3)],
        ],
    ),
)
assert move_robots(robots, Map(11, 7), seconds=100) == [
    (0, 2),
    (1, 3),
    (1, 6),
    (2, 3),
    (3, 5),
    (4, 5),
    (4, 5),
    (5, 4),
    (6, 0),
    (6, 0),
    (6, 6),
    (9, 0),
]
assert _get_quadrants(Map(3, 3)) == [
    ((0, 0), (1, 1)),  # top left
    ((2, 0), (3, 1)),  # top right
    ((0, 2), (1, 3)),  # bottom left
    ((2, 2), (3, 3)),  # bottom right
]
assert _get_quadrants(Map(4, 3)) == [
    ((0, 0), (2, 1)),  # top left
    ((2, 0), (4, 1)),  # top right
    ((0, 2), (2, 3)),  # bottom left
    ((2, 2), (4, 3)),  # bottom right
]
assert _get_quadrants(Map(3, 4)) == [
    ((0, 0), (1, 2)),  # top left
    ((2, 0), (3, 2)),  # top right
    ((0, 2), (1, 4)),  # bottom left
    ((2, 2), (3, 4)),  # bottom right
]

positions = move_robots(robots, Map(11, 7), seconds=100)
assert find_safety_factor(positions, Map(11, 7)) == 12

robots = []
with open("2024/14_restroom_redoubt/input.txt") as f:
    for line in f:
        start_x, start_y, moves_x, moves_y = map(int, re.findall(r"[\d-]+", line))
        robots.append(_gen_robot((start_x, start_y), (moves_x, moves_y)))

mover = _gen_move_robots(robots, Map(101, 103))
for positions in _find_xmas_tree(mover, Map(101, 103)):
    _draw_positions(positions, Map(101, 103))
    input("continue?")
    print()
