"""
"Looks like the Chief's not here. Next!"
One of The Historians pulls out a device and pushes the only button on it.
After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues,
a small Elf who lives on the station tugs on your shirt;
she'd like to know if you could help her with her word search (your puzzle input).
She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal,
written backwards, or even overlapping other words.
It's a little unusual, though, as you don't merely need to find one instance of XMAS -
you need to find all of them.
Here are a few ways XMAS might appear,
where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX

In this word search, XMAS occurs a total of 18 times;
here's the same word search again,
but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?
"""

from enum import StrEnum, auto
from textwrap import dedent


class Match(StrEnum):
    HORIZONTAL_FORWARDS = auto()
    HORIZONTAL_BACKWARDS = auto()
    VERTICAL_FORWARDS = auto()
    VERTICAL_BACKWARDS = auto()
    DIAGONAL_LR_FORWARDS = auto()
    DIAGONAL_LR_BACKWARDS = auto()
    DIAGONAL_RL_FORWARDS = auto()
    DIAGONAL_RL_BACKWARDS = auto()


def ceres_search(data):
    matches = []

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "X":
                matches.extend(_apply_rules(data, i, j))

    return matches


RULES = [
    (
        # XMAS
        Match.HORIZONTAL_FORWARDS,
        lambda data, i, j: j + 3 < len(data[i]),
        [(0, +1), (0, +2), (0, +3)],
    ),
    (
        # SAMX
        Match.HORIZONTAL_BACKWARDS,
        lambda data, i, j: j - 3 >= 0,
        [(0, -1), (0, -2), (0, -3)],
    ),
    (
        # X
        # M
        # A
        # S
        Match.VERTICAL_FORWARDS,
        lambda data, i, j: i + 3 < len(data),
        [(+1, 0), (+2, 0), (+3, 0)],
    ),
    (
        # S
        # A
        # M
        # X
        Match.VERTICAL_BACKWARDS,
        lambda data, i, j: i - 3 >= 0,
        [(-1, 0), (-2, 0), (-3, 0)],
    ),
    (
        # X...
        # .M..
        # ..A.
        # ...S
        Match.DIAGONAL_LR_FORWARDS,
        lambda data, i, j: i + 3 < len(data) and j + 3 < len(data[i]),
        [(+1, +1), (+2, +2), (+3, +3)],
    ),
    (
        # S...
        # .A..
        # ..M.
        # ...X
        Match.DIAGONAL_LR_BACKWARDS,
        lambda data, i, j: i - 3 >= 0 and j - 3 >= 0,
        [(-1, -1), (-2, -2), (-3, -3)],
    ),
    (
        # ...X
        # ..M.
        # .A..
        # S...
        Match.DIAGONAL_RL_FORWARDS,
        lambda data, i, j: i + 3 < len(data) and j - 3 >= 0,
        [(+1, -1), (+2, -2), (+3, -3)],
    ),
    (
        # ...S
        # ..A.
        # .M..
        # X...
        Match.DIAGONAL_RL_BACKWARDS,
        lambda data, i, j: i - 3 >= 0 and j + 3 < len(data[i]),
        [(-1, +1), (-2, +2), (-3, +3)],
    ),
]


def _apply_rules(data, i, j):
    for name, checker, indexes in RULES:
        m_index, a_index, s_index = indexes

        if (
            checker(data, i, j)
            and data[i + m_index[0]][j + m_index[1]] == "M"
            and data[i + a_index[0]][j + a_index[1]] == "A"
            and data[i + s_index[0]][j + s_index[1]] == "S"
        ):
            yield name


def _to_array(s: str):
    return dedent(s).strip().splitlines()


s = _to_array(
    """
    XMAS
    """,
)
assert ceres_search(s) == [Match.HORIZONTAL_FORWARDS]

s = _to_array(
    """
    SAMX
    """,
)
assert ceres_search(s) == [Match.HORIZONTAL_BACKWARDS]

s = _to_array(
    """
    SAMXMAS
    """,
)
assert ceres_search(s) == [Match.HORIZONTAL_FORWARDS, Match.HORIZONTAL_BACKWARDS]

s = _to_array(
    """
    XMASAMX
    """,
)
assert ceres_search(s) == [Match.HORIZONTAL_FORWARDS, Match.HORIZONTAL_BACKWARDS]

s = _to_array(
    """
    X
    M
    A
    S
    """,
)
assert ceres_search(s) == [Match.VERTICAL_FORWARDS]

s = _to_array(
    """
    S
    A
    M
    X
    """,
)
assert ceres_search(s) == [Match.VERTICAL_BACKWARDS]

s = _to_array(
    """
    S
    A
    M
    X
    M
    A
    S
    """,
)
assert ceres_search(s) == [Match.VERTICAL_FORWARDS, Match.VERTICAL_BACKWARDS]

s = _to_array(
    """
    X
    M
    A
    S
    A
    M
    X
    """,
)
assert ceres_search(s) == [Match.VERTICAL_FORWARDS, Match.VERTICAL_BACKWARDS]

s = _to_array(
    """
    X...
    .M..
    ..A.
    ...S
    """,
)
assert ceres_search(s) == [Match.DIAGONAL_LR_FORWARDS]

s = _to_array(
    """
    S...
    .A..
    ..M.
    ...X
    """,
)
assert ceres_search(s) == [Match.DIAGONAL_LR_BACKWARDS]

s = _to_array(
    """
    X......
    .M.....
    ..A....
    ...S...
    ....A..
    .....M.
    ......X
    """,
)
assert ceres_search(s) == [Match.DIAGONAL_LR_FORWARDS, Match.DIAGONAL_LR_BACKWARDS]

s = _to_array(
    """
    S......
    .A.....
    ..M....
    ...X...
    ....M..
    .....A.
    ......S
    """,
)
assert ceres_search(s) == [Match.DIAGONAL_LR_FORWARDS, Match.DIAGONAL_LR_BACKWARDS]

s = _to_array(
    """
    ...X
    ..M.
    .A..
    S...
    """,
)
assert ceres_search(s) == [Match.DIAGONAL_RL_FORWARDS]

s = _to_array(
    """
    ...S
    ..A.
    .M..
    X...
    """,
)
assert ceres_search(s) == [Match.DIAGONAL_RL_BACKWARDS]

s = _to_array(
    """
    ......X
    .....M.
    ....A..
    ...S...
    ..A....
    .M.....
    X......
    """,
)
assert ceres_search(s) == [Match.DIAGONAL_RL_FORWARDS, Match.DIAGONAL_RL_BACKWARDS]

s = _to_array(
    """
    ......S
    .....A.
    ....M..
    ...X...
    ..M....
    .A.....
    S......
    """,
)
assert ceres_search(s) == [Match.DIAGONAL_RL_FORWARDS, Match.DIAGONAL_RL_BACKWARDS]

s = _to_array(
    """
    ..X...
    .SAMX.
    .A..A.
    XMAS.S
    .X....
    """,
)
assert ceres_search(s) == [
    Match.DIAGONAL_LR_FORWARDS,
    Match.HORIZONTAL_BACKWARDS,
    Match.HORIZONTAL_FORWARDS,
    Match.VERTICAL_BACKWARDS,
]

with open("4_ceres_search_input.txt") as f:
    print(len(ceres_search(_to_array(f.read()))))
