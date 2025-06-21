"""
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions,
you flip over the word search to find that this isn't actually an XMAS puzzle;
it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X.
One way to achieve that is like this:

M.S
.A.
M.S

Irrelevant characters have again been replaced with . in the above diagram.
Within the X, each MAS can be written forwards or backwards.

Here's the same example from before,
but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........

In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over
to the word search side and try again.
How many times does an X-MAS appear?
"""

from enum import StrEnum, auto
from textwrap import dedent


class Match(StrEnum):
    MAS_MAS = auto()
    MAS_SAM = auto()
    SAM_MAS = auto()
    SAM_SAM = auto()


def ceres_search_mas(data):
    matches = []

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "A":
                matches.extend(_apply_rules(data, i, j))

    return matches


RULES = [
    (
        # M.M
        # .A.
        # S.S
        Match.MAS_MAS,
        "MMSS",
    ),
    (
        # M.S
        # .A.
        # M.S
        Match.MAS_SAM,
        "MSMS",
    ),
    (
        # S.M
        # .A.
        # S.M
        Match.SAM_MAS,
        "SMSM",
    ),
    (
        # S.S
        # .A.
        # M.M
        Match.SAM_SAM,
        "SSMM",
    ),
]


def _apply_rules(data, i, j):
    if not (i - 1 >= 0 and i + 1 < len(data) and j - 1 >= 0 and j + 1 < len(data[i])):
        return

    for name, ordered_chars in RULES:
        ul, ur, ll, lr = ordered_chars
        if (
            data[i - 1][j - 1] == ul
            and data[i - 1][j + 1] == ur
            and data[i + 1][j - 1] == ll
            and data[i + 1][j + 1] == lr
        ):
            yield name


def _to_array(s: str):
    return dedent(s).strip().splitlines()


s = _to_array(
    """
    M.M
    .A.
    S.S
    """,
)
assert ceres_search_mas(s) == [Match.MAS_MAS]


s = _to_array(
    """
    M.S
    .A.
    M.S
    """,
)
assert ceres_search_mas(s) == [Match.MAS_SAM]


s = _to_array(
    """
    S.M
    .A.
    S.M
    """,
)
assert ceres_search_mas(s) == [Match.SAM_MAS]


s = _to_array(
    """
    S.S
    .A.
    M.M
    """,
)
assert ceres_search_mas(s) == [Match.SAM_SAM]

s = _to_array(
    """
    .M.S......
    ..A..MSMS.
    .M.S.MAA..
    ..A.ASMSM.
    .M.S.M....
    ..........
    S.S.S.S.S.
    .A.A.A.A..
    M.M.M.M.M.
    ..........
    """,
)
assert ceres_search_mas(s) == [
    Match.MAS_SAM,
    Match.MAS_MAS,
    Match.SAM_SAM,
    Match.MAS_SAM,
    Match.SAM_MAS,
    Match.SAM_SAM,
    Match.SAM_SAM,
    Match.SAM_SAM,
    Match.SAM_SAM,
]

with open("04_ceres_search/input.txt") as f:
    print(len(ceres_search_mas(_to_array(f.read()))))
