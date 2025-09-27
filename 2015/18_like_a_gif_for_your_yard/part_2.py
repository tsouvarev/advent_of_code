"""
You flip the instructions over; Santa goes on to point out that
this is all just an implementation of Conway's Game of Life.
At least, it was, until you notice that
something's wrong with the grid of lights you bought:
four lights, one in each corner, are stuck on and can't be turned off.
The example above will actually run like this:

Initial state:
##.#.#
...##.
#....#
..#...
#.#..#
####.#

After 1 step:
#.##.#
####.#
...##.
......
#...#.
#.####

After 2 steps:
#..#.#
#....#
.#.##.
...##.
.#..##
##.###

After 3 steps:
#...##
####.#
..##.#
......
##....
####.#

After 4 steps:
#.####
#....#
...#..
.##...
#.....
#.#..#

After 5 steps:
##.###
.##..#
.##...
.##...
#.#...
##...#

After 5 steps, this example now has 17 lights on.

In your grid of 100x100 lights, given your initial configuration,
but with the four corners always in the on state,
how many lights are on after 100 steps?
"""

from textwrap import dedent

type Field = list[list[bool]]


def switch_lights(field: Field) -> Field:
    new_field = []
    corners = {
        (0, 0),
        (0, len(field[0]) - 1),
        (len(field) - 1, 0),
        (len(field) - 1, len(field[0]) - 1),
    }

    for i in range(len(field)):
        new_row = []

        for j in range(len(field[i])):
            new_row.append((i, j) in corners or _get_new_state(field, i, j))

        new_field.append(new_row)

    return new_field


def count_lights(field: Field) -> int:
    return sum(1 for row in field for col in row if col)


def _get_new_state(field: Field, i: int, j: int) -> bool:
    neighbors = [
        _get_index_safe(field, i - 1, j - 1),
        _get_index_safe(field, i - 1, j),
        _get_index_safe(field, i - 1, j + 1),
        _get_index_safe(field, i, j - 1),
        _get_index_safe(field, i, j + 1),
        _get_index_safe(field, i + 1, j - 1),
        _get_index_safe(field, i + 1, j),
        _get_index_safe(field, i + 1, j + 1),
    ]
    count_of_ons = neighbors.count(True)

    if field[i][j]:
        return count_of_ons in {2, 3}
    return count_of_ons == 3


def _get_index_safe(field: Field, i: int, j: int, default: bool = False) -> bool:
    if 0 <= i < len(field) and 0 <= j < len(field[i]):
        return field[i][j]

    return default


def _to_array(s: str) -> Field:
    return [[l == "#" for l in line] for line in dedent(s).strip().splitlines()]


def _to_map(field: Field) -> str:
    res = ""

    for row in field:
        for col in row:
            res += "#" if col else "."
        res += "\n"

    return res


def _check_switch(raw_field: str) -> str:
    mapped = _to_map(switch_lights(_to_array(raw_field)))
    return f"\n{mapped}"


field = """
    ##.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####.#
    """
assert _check_switch(field) == dedent(
    """
    #.##.#
    ####.#
    ...##.
    ......
    #...#.
    #.####
    """,
)

field = """
    #.##.#
    ####.#
    ...##.
    ......
    #...#.
    #.####
    """
assert _check_switch(field) == dedent(
    """
    #..#.#
    #....#
    .#.##.
    ...##.
    .#..##
    ##.###
    """,
)

field = """
    #..#.#
    #....#
    .#.##.
    ...##.
    .#..##
    ##.###
    """
assert _check_switch(field) == dedent(
    """
    #...##
    ####.#
    ..##.#
    ......
    ##....
    ####.#
    """,
)

field = """
    #...##
    ####.#
    ..##.#
    ......
    ##....
    ####.#
    """
assert _check_switch(field) == dedent(
    """
    #.####
    #....#
    ...#..
    .##...
    #.....
    #.#..#
    """,
)

field = """
    #.####
    #....#
    ...#..
    .##...
    #.....
    #.#..#
    """
assert _check_switch(field) == dedent(
    """
    ##.###
    .##..#
    .##...
    .##...
    #.#...
    ##...#
    """,
)


with open("2015/18_like_a_gif_for_your_yard/input.txt") as f:
    field = _to_array(f.read())

    # constant lights in the corners
    field[0][0], field[0][99], field[99][0], field[99][99] = True, True, True, True

    for _ in range(100):
        field = switch_lights(field)

    print(count_lights(field))
