"""
Crossing the bridge, you've barely reached the other side of the stream
when a program comes up to you, clearly in distress.
"It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such
that adjacent hexes can be found to the north, northeast,
southeast, south, southwest, and northwest:

  \\ n  /
 nw +--+ ne
   /    \
 -+      +-
  \\    /
 sw +--+ se
   / s  \



You have the path the child process took.
Starting where he started, you need to determine the fewest number of steps
required to reach him.
(A "step" means to move from the hex you are in to any adjacent hex.)

For example:

- ne,ne,ne is 3 steps away.
- ne,ne,sw,sw is 0 steps away (back where you started).
- ne,ne,s,s is 2 steps away (se,se).
- se,sw,se,sw,sw is 3 steps away (s,s,sw).
"""

from enum import StrEnum, auto
from itertools import accumulate

type Step = tuple[int, int, int]


class Dir(StrEnum):
    N = auto()
    NE = auto()
    SE = auto()
    S = auto()
    SW = auto()
    NW = auto()


AXIAL_COORD_MAP: dict[Dir, Step] = {
    Dir.N: (0, 1, -1),
    Dir.S: (0, -1, 1),
    Dir.NE: (1, 0, -1),
    Dir.SW: (-1, 0, 1),
    Dir.NW: (-1, 1, 0),
    Dir.SE: (1, -1, 0),
}


def solve(raw_steps: str) -> tuple[int, int]:
    steps = _parse_steps(raw_steps)

    sum_steps = _move(*steps)
    distances = accumulate(steps, _move)

    return _get_axial_dist(sum_steps), max(map(_get_axial_dist, distances))


def _move(*steps: Step) -> Step:
    return tuple(map(sum, zip(*steps)))  # type: ignore[invalid-return-value]


def _get_axial_dist(step: Step) -> int:
    return sum(map(abs, step)) / 2


def _parse_steps(raw_steps: str) -> list[Step]:
    return [AXIAL_COORD_MAP[Dir(step)] for step in raw_steps.split(",")]


assert _move((0, 1, -1), (0, 1, -1)) == (0, 2, -2)


assert solve("ne,ne,ne") == (3, 3)
assert solve("ne,ne,sw,sw") == (0, 2)
assert solve("ne,ne,s,s") == (2, 2)
assert solve("se,sw,se,sw,sw") == (3, 3)


with open("2017/11_hex_ed/input.txt") as f:
    print(solve(f.read()))
