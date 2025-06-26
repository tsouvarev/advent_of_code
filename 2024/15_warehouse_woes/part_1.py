"""
You appear back inside your own mini submarine!
Each Historian drives their mini submarine in a different direction;
maybe the Chief has his own submarine down here somewhere as well?

You look up to see a vast school of lanternfish swimming past you.
On closer inspection, they seem quite anxious,
so you drive your mini submarine over to see if you can help.

Because lanternfish populations grow rapidly, they need a lot of food,
and that food needs to be stored somewhere.
That's why these lanternfish have built elaborate warehouse complexes
operated by robots!

These lanternfish seem so anxious because they have lost control of the robot
that operates one of their most important warehouses!
It is currently running amok, pushing around boxes in the warehouse
with no regard for lanternfish logistics or lanternfish inventory management strategies.

Right now, none of the lanternfish are brave enough
to swim up to an unpredictable robot so they could shut it off.
However, if you could anticipate the robot's movements,
maybe they could find a safe option.

The lanternfish already have a map of the warehouse
and a list of movements the robot will attempt to make (your puzzle input).
The problem is that the movements will sometimes fail as boxes are shifted around,
making the actual movements of the robot difficult to predict.

For example:

##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^

As the robot (@) attempts to move, if there are any boxes (O) in the way,
the robot will also attempt to push those boxes.
However, if this action would cause the robot or a box to move into a wall (#),
nothing moves instead, including the robot.
The initial positions of these are shown on the map
at the top of the document the lanternfish gave you.

The rest of the document describes the moves
(^ for up, v for down, < for left, > for right)
that the robot will attempt to make, in order.
(The moves form a single giant sequence;
they are broken into multiple lines just to make copy-pasting easier.
Newlines within the move sequence should be ignored.)

Here is a smaller example to get started:

########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<

Were the robot to attempt the given sequence of moves,
it would push around the boxes as follows:

Initial state:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move <:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#..@OO.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.@...#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#..@O..#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#...@O.#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#....@O#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#.....O#
#.#.O@.#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

The larger example has many more moves;
after the robot has finished those moves, the warehouse would look like this:

##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########

The lanternfish use their own custom Goods Positioning System (GPS for short)
to track the locations of the boxes.
The GPS coordinate of a box is equal to
100 times its distance from the top edge of the map
plus its distance from the left edge of the map.
(This process does not stop at wall tiles;
measure all the way to the edges of the map.)

So, the box shown below has a distance of 1 from the top edge of the map
and 4 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 4 = 104.

#######
#...O..
#......

The lanternfish would like to know
the sum of all boxes' GPS coordinates after the robot finishes moving.
In the larger example, the sum of all boxes' GPS coordinates is 10092.
In the smaller example, the sum is 2028.

Predict the motion of the robot and boxes in the warehouse.
After the robot is finished moving, what is the sum of all boxes' GPS coordinates?
"""

from enum import StrEnum
from textwrap import dedent
from typing import NamedTuple

from pytest import mark

type WareHouse = list[list[str]]


class Point(NamedTuple):
    x: int
    y: int


class Direction(StrEnum):
    LEFT = "<"
    RIGHT = ">"
    UP = "^"
    DOWN = "v"


def move(warehouse: WareHouse, directions: list[Direction]) -> WareHouse:
    for direction in directions:
        start = _find_start(warehouse)
        match direction:
            case Direction.LEFT:
                warehouse = _move_left(warehouse, start)
            case Direction.RIGHT:
                warehouse = _move_right(warehouse, start)
            case Direction.UP:
                warehouse = _move_up(warehouse, start)
            case Direction.DOWN:
                warehouse = _move_down(warehouse, start)

    return warehouse


def sum_coordinates(warehouse: WareHouse) -> int:
    res = 0

    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "O":
                res += 100 * i + j

    return res


def _find_start(warehouse: WareHouse) -> Point:
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "@":
                return Point(i, j)

    msg = "No start"
    raise ValueError(msg)


def _move_left(warehouse: WareHouse, point: Point) -> WareHouse:
    moving_to = _get_left_shift_to(warehouse, point)

    if moving_to is None:
        return warehouse

    warehouse[point.x][point.y] = "."
    warehouse[point.x][moving_to.y] = warehouse[point.x][moving_to.y + 1]
    warehouse[point.x][point.y - 1] = "@"

    return warehouse


def _get_left_shift_to(warehouse: WareHouse, point: Point) -> Point | None:
    for j in range(point.y - 1, 0, -1):
        if warehouse[point.x][j] == ".":
            return Point(point.x, j)

        if warehouse[point.x][j] == "#":
            break

    return None


def _move_right(warehouse: WareHouse, point: Point) -> WareHouse:
    moving_to = _get_right_shift_to(warehouse, point)

    if moving_to is None:
        return warehouse

    warehouse[point.x][point.y] = "."
    warehouse[point.x][moving_to.y] = warehouse[point.x][moving_to.y - 1]
    warehouse[point.x][point.y + 1] = "@"

    return warehouse


def _get_right_shift_to(warehouse: WareHouse, point: Point) -> Point | None:
    for j in range(point.y + 1, len(warehouse[point.x])):
        if warehouse[point.x][j] == ".":
            return Point(point.x, j)

        if warehouse[point.x][j] == "#":
            break

    return None


def _move_up(warehouse: WareHouse, point: Point) -> WareHouse:
    moving_to = _get_up_shift_to(warehouse, point)

    if moving_to is None:
        return warehouse

    warehouse[point.x][point.y] = "."
    warehouse[moving_to.x][point.y] = warehouse[moving_to.x + 1][point.y]
    warehouse[point.x - 1][point.y] = "@"

    return warehouse


def _get_up_shift_to(warehouse: WareHouse, point: Point) -> Point | None:
    for i in range(point.x - 1, 0, -1):
        if warehouse[i][point.y] == ".":
            return Point(i, point.y)

        if warehouse[i][point.y] == "#":
            break

    return None


def _move_down(warehouse: WareHouse, point: Point) -> WareHouse:
    moving_to = _get_down_shift_to(warehouse, point)

    if moving_to is None:
        return warehouse

    warehouse[point.x][point.y] = "."
    warehouse[moving_to.x][point.y] = warehouse[moving_to.x - 1][point.y]
    warehouse[point.x + 1][point.y] = "@"

    return warehouse


def _get_down_shift_to(warehouse: WareHouse, point: Point) -> Point | None:
    for i in range(point.x + 1, len(warehouse)):
        if warehouse[i][point.y] == ".":
            return Point(i, point.y)

        if warehouse[i][point.y] == "#":
            break

    return None


def _to_array(s: str):
    return [list(l) for l in dedent(s).strip().splitlines()]


@mark.parametrize(
    ("from_", "to_"),
    [
        ("#.@", "#@."),  # simple
        ("#.O@", "#O@."),  # move one box
        ("#.OO@", "#OO@."),  # move two boxes
        ("#@", "#@"),  # hit wall
        ("#O@", "#O@"),  # hit wall with box
        ("#OO@", "#OO@"),  # hit wall with two boxes
    ],
)
def test_move_left(from_, to_):
    from_as_array = _to_array(from_)
    start = _find_start(from_as_array)
    assert _move_left(from_as_array, start) == _to_array(to_)


@mark.parametrize(
    ("from_", "to_"),
    [
        ("@.#", ".@#"),  # simple
        ("@O.#", ".@O#"),  # move one box
        ("@OO.#", ".@OO#"),  # move two boxes
        ("@#", "@#"),  # hit wall
        ("@O#", "@O#"),  # hit wall with box
        ("@OO#", "@OO#"),  # hit wall with two boxes
    ],
)
def test_move_right(from_, to_):
    from_as_array = _to_array(from_)
    start = _find_start(from_as_array)
    assert _move_right(from_as_array, start) == _to_array(to_)


@mark.parametrize(
    ("from_", "to_"),
    [
        # simple
        (
            """
            #
            .
            @
            """,
            """
            #
            @
            .
            """,
        ),
        # move one box
        (
            """
            #
            .
            O
            @
            """,
            """
            #
            O
            @
            .
            """,
        ),
        # move two boxes
        (
            """
            #
            .
            O
            O
            @
            """,
            """
            #
            O
            O
            @
            .
            """,
        ),
        # hit wall
        (
            """
            #
            @
            """,
            """
            #
            @
            """,
        ),
        # hit wall with box
        (
            """
            #
            O
            @
            """,
            """
            #
            O
            @
            """,
        ),
        # hit wall with two boxes
        (
            """
            #
            O
            O
            @
            """,
            """
            #
            O
            O
            @
            """,
        ),
    ],
)
def test_move_up(from_, to_):
    from_as_array = _to_array(from_)
    start = _find_start(from_as_array)
    assert _move_up(from_as_array, start) == _to_array(to_)


@mark.parametrize(
    ("from_", "to_"),
    [
        # simple
        (
            """
            @
            .
            #
            """,
            """
            .
            @
            #
            """,
        ),
        # move one box
        (
            """
            @
            O
            .
            #
            """,
            """
            .
            @
            O
            #
            """,
        ),
        # move two boxes
        (
            """
            @
            O
            O
            .
            #
            """,
            """
            .
            @
            O
            O
            #
            """,
        ),
        # hit wall
        (
            """
            @
            #
            """,
            """
            @
            #
            """,
        ),
        # hit wall with box
        (
            """
            @
            O
            #
            """,
            """
            @
            O
            #
            """,
        ),
        # hit wall with two boxes
        (
            """
            @
            O
            O
            #
            """,
            """
            @
            O
            O
            #
            """,
        ),
    ],
)
def test_move_down(from_, to_):
    from_as_array = _to_array(from_)
    start = _find_start(from_as_array)
    assert _move_down(from_as_array, start) == _to_array(to_)


s = _to_array(
    """
    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########
    """,
)
assert move(s, "<^^>>>vv<v>>v<<") == _to_array(
    """
    ########
    #....OO#
    ##.....#
    #.....O#
    #.#O@..#
    #...O..#
    #...O..#
    ########
    """,
)

s = _to_array(
    """
    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########
    """,
)
directions = (
    "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^"
    "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v"
    "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<"
    "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^"
    "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><"
    "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^"
    ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^"
    "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>"
    "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>"
    "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"
)
assert move(s, directions) == _to_array(
    """
    ##########
    #.O.O.OOO#
    #........#
    #OO......#
    #OO@.....#
    #O#.....O#
    #O.....OO#
    #O.....OO#
    #OO....OO#
    ##########
    """,
)

s = _to_array(
    """
    ########
    #....OO#
    ##.....#
    #.....O#
    #.#O@..#
    #...O..#
    #...O..#
    ########
    """,
)
assert sum_coordinates(s) == 2028

s = _to_array(
    """
    ##########
    #.O.O.OOO#
    #........#
    #OO......#
    #OO@.....#
    #O#.....O#
    #O.....OO#
    #O.....OO#
    #OO....OO#
    ##########
    """,
)
assert sum_coordinates(s) == 10092

with open("2024/15_warehouse_woes/input_map.txt") as f:
    warehouse = _to_array(f.read())

with open("2024/15_warehouse_woes/input_moves.txt") as f:
    directions = f.read()

print(sum_coordinates(move(warehouse, directions)))
