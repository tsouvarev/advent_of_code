"""
One of The Historians needs to use the bathroom;
fortunately, you know there's a bathroom near an unvisited location on their list,
and so you're all quickly teleported directly to the lobby of Easter Bunny Headquarters.

Unfortunately, EBHQ seems to have "improved" bathroom security again
after your last visit. The area outside the bathroom is swarming with robots!

To get The Historian safely to the bathroom,
you'll need a way to predict where the robots will be in the future.
Fortunately, they all seem to be moving on the tile floor in predictable straight lines.

You make a list (your puzzle input)
of all of the robots' current positions (p) and velocities (v), one robot per line.
For example:

p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3

Each robot's position is given as p=x,y
where x represents the number of tiles the robot is from the left wall
and y represents the number of tiles from the top wall (when viewed from above).
So, a position of p=0,0 means the robot is all the way in the top-left corner.

Each robot's velocity is given as v=x,y where x and y are given in tiles per second.
Positive x means the robot is moving to the right,
and positive y means the robot is moving down.
So, a velocity of v=1,-2 means that each second,
the robot moves 1 tile to the right and 2 tiles up.

The robots outside the actual bathroom
are in a space which is 101 tiles wide and 103 tiles tall (when viewed from above).
However, in this example, the robots are in a space
which is only 11 tiles wide and 7 tiles tall.

The robots are good at navigating over/under each other
(due to a combination of springs, extendable legs, and quadcopters),
so they can share the same tile and don't interact with each other.
Visually, the number of robots on each tile in this example looks like this:

1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...

These robots have a unique feature for maximum bathroom security: they can teleport.
When a robot would run into an edge of the space they're in,
they instead teleport to the other side, effectively wrapping around the edges.
Here is what robot p=2,4 v=2,-3 does for the first few seconds:

Initial state:
...........
...........
...........
...........
..1........
...........
...........

After 1 second:
...........
....1......
...........
...........
...........
...........
...........

After 2 seconds:
...........
...........
...........
...........
...........
......1....
...........

After 3 seconds:
...........
...........
........1..
...........
...........
...........
...........

After 4 seconds:
...........
...........
...........
...........
...........
...........
..........1

After 5 seconds:
...........
...........
...........
.1.........
...........
...........
...........

The Historian can't wait much longer,
so you don't have to simulate the robots for very long.
Where will the robots be after 100 seconds?

In the above example, the number of robots on each tile
after 100 seconds has elapsed looks like this:

......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....

To determine the safest area,
count the number of robots in each quadrant after 100 seconds.
Robots that are exactly in the middle (horizontally or vertically)
don't count as being in any quadrant, so the only relevant robots are:

..... 2..1.
..... .....
1.... .....

..... .....
...12 .....
.1... 1....

In this example, the quadrants contain 1, 3, 4, and 1 robot.
Multiplying these together gives a total safety factor of 12.

Predict the motion of the robots in your list
within a space which is 101 tiles wide and 103 tiles tall.
What will the safety factor be after exactly 100 seconds have elapsed?
"""

import re
from collections import Counter, defaultdict
from functools import reduce
from itertools import count, starmap
from operator import mul
from typing import NamedTuple


class Robot(NamedTuple):
    start: "Coordinate"
    moves: "Move"


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


def _gen_move(start, moves, tile_map):
    for i in count(1):
        yield move_robot(_gen_robot(start, moves), Map(*tile_map), seconds=i)


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


robot = _gen_move((2, 4), (2, -3), (11, 7))
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

    positions = move_robots(robots, Map(101, 103), seconds=100)
    print(find_safety_factor(positions, Map(101, 103)))
