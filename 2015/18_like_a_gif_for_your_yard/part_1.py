"""
After the million lights incident, the fire code has gotten stricter:
now, at most ten thousand lights are allowed. You arrange them in a 100x100 grid.

Never one to let you down,
Santa again mails you instructions on the ideal lighting configuration.
With so few lights, he says, you'll have to resort to animation.

Start by setting your lights to the included initial configuration (your puzzle input).
A # means "on", and a . means "off".

Then, animate your grid in steps,
where each step decides the next configuration based on the current one.
Each light's next state (either on or off) depends on its current state
and the current states of the eight lights adjacent to it (including diagonals).
Lights on the edge of the grid might have fewer than eight neighbors;
the missing ones always count as "off".

For example, in a simplified 6x6 grid,
the light marked A has the neighbors numbered 1 through 8,
and the light marked B, which is on an edge, only has the neighbors marked 1 through 5:

1B5...
234...
......
..123.
..8A4.
..765.

The state a light should have next is based on its current state (on or off)
plus the number of neighbors that are on:

-   A light which is on stays on when 2 or 3 neighbors are on,
    and turns off otherwise.
-   A light which is off turns on if exactly 3 neighbors are on,
    and stays off otherwise.

All of the lights update simultaneously;
they all consider the same current state before moving to the next.

Here's a few steps from an example configuration of another 6x6 grid:

Initial state:
.#.#.#
...##.
#....#
..#...
#.#..#
####..

After 1 step:
..##..
..##.#
...##.
......
#.....
#.##..

After 2 steps:
..###.
......
..###.
......
.#....
.#....

After 3 steps:
...#..
......
...#..
..##..
......
......

After 4 steps:
......
......
..##..
..##..
......
......

After 4 steps, this example has four lights on.

In your grid of 100x100 lights, given your initial configuration,
how many lights are on after 100 steps?
"""

from textwrap import dedent

type Field = list[list[bool]]


def switch_lights(field: Field) -> Field:
    new_field = []

    for i in range(len(field)):
        new_row = []

        for j in range(len(field[i])):
            new_row.append(_get_new_state(field, i, j))

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


field = _to_array(
    """
    ...
    .#.
    ...
    """,
)
assert _get_new_state(field, 1, 1) is False


field = _to_array(
    """
    ...
    .##
    ...
    """,
)
assert _get_new_state(field, 1, 1) is False

field = _to_array(
    """
    .#.
    .##
    ...
    """,
)
assert _get_new_state(field, 1, 1) is True

field = _to_array(
    """
    .#.
    .##
    .#.
    """,
)
assert _get_new_state(field, 1, 1) is True

field = _to_array(
    """
    .#.
    ###
    .#.
    """,
)
assert _get_new_state(field, 1, 1) is False

field = _to_array(
    """
    ...
    ...
    ...
    """,
)
assert _get_new_state(field, 1, 1) is False

field = _to_array(
    """
    .#.
    ...
    ...
    """,
)
assert _get_new_state(field, 1, 1) is False

field = _to_array(
    """
    .#.
    ..#
    ...
    """,
)
assert _get_new_state(field, 1, 1) is False

field = _to_array(
    """
    .#.
    ..#
    .#.
    """,
)
assert _get_new_state(field, 1, 1) is True

field = _to_array(
    """
    .#.
    #.#
    .#.
    """,
)
assert _get_new_state(field, 1, 1) is False

field = _to_array(
    """
    ...
    ...
    ...
    """,
)
assert _get_new_state(field, 0, 0) is False
assert _get_new_state(field, 0, 2) is False
assert _get_new_state(field, 2, 0) is False
assert _get_new_state(field, 2, 2) is False

field = """
    .#.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####..
    """
assert _check_switch(field) == dedent(
    """
    ..##..
    ..##.#
    ...##.
    ......
    #.....
    #.##..
    """,
)

field = """
    ..##..
    ..##.#
    ...##.
    ......
    #.....
    #.##..
    """
assert _check_switch(field) == dedent(
    """
    ..###.
    ......
    ..###.
    ......
    .#....
    .#....
    """,
)

field = """
    ..###.
    ......
    ..###.
    ......
    .#....
    .#....
    """
assert _check_switch(field) == dedent(
    """
    ...#..
    ......
    ...#..
    ..##..
    ......
    ......
    """,
)

field = """
    ...#..
    ......
    ...#..
    ..##..
    ......
    ......
    """
assert _check_switch(field) == dedent(
    """
    ......
    ......
    ..##..
    ..##..
    ......
    ......
    """,
)


with open("2015/18_like_a_gif_for_your_yard/input.txt") as f:
    field = _to_array(f.read())

    for _ in range(100):
        field = switch_lights(field)

    print(count_lights(field))
