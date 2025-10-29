"""
After getting the first capsule (it contained a star! what great fortune!),
the machine detects your success and begins to rearrange itself.

When it's done,
the discs are back in their original configuration as if it were time=0 again,
but a new disc with 11 positions and starting at position 0
has appeared exactly one second below the previously-bottom disc.

With this new disc, and counting again starting from time=0
with the configuration in your puzzle input,
what is the first time you can press the button to get another capsule?
"""

from itertools import count
from typing import NamedTuple

from parse import parse


class Disc(NamedTuple):
    n: int
    num_slots: int
    started_at: int


def solve(discs: list[Disc]) -> int:
    for ts in count(1):
        print(ts)
        if _is_fall_through(discs, ts):
            return ts
    raise ValueError


def _is_fall_through(discs: list[Disc], ts: int) -> bool:
    disc_positions = (_get_position(disc, ts) for disc in discs)
    first = next(disc_positions)
    return all(first == x for x in disc_positions)


def _get_position(disc: Disc, ts: int) -> int:
    return (ts + disc.n + disc.started_at) % disc.num_slots


disc_1 = Disc(n=1, num_slots=5, started_at=4)
disc_2 = Disc(n=2, num_slots=2, started_at=1)
discs = [disc_1, disc_2]

assert _get_position(disc_1, 0) == 0
assert _get_position(disc_2, 0) == 1
assert _get_position(disc_1, 5) == 0
assert _get_position(disc_2, 5) == 0

assert _is_fall_through(discs, 0) is False
assert _is_fall_through(discs, 5) is True

assert solve(discs) == 5

with open("2016/15_timing_is_everything/input.txt") as f:
    spec = "Disc #{:d} has {:d} positions; at time=0, it is at position {:d}."

    discs = [Disc(*parse(spec, line.strip()).fixed) for line in f]
    discs.append(Disc(n=7, num_slots=11, started_at=0))

    print(solve(discs))
