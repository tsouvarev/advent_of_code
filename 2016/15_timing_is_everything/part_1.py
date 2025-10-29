"""
The halls open into an interior plaza containing a large kinetic sculpture.
The sculpture is in a sealed enclosure
and seems to involve a set of identical spherical capsules
that are carried to the top and allowed to bounce through the maze of spinning pieces.

Part of the sculpture is even interactive!
When a button is pressed, a capsule is dropped
and tries to fall through slots in a set of rotating discs
to finally go through a little hole at the bottom and come out of the sculpture.
If any of the slots aren't aligned with the capsule as it passes,
the capsule bounces off the disc and soars away.
You feel compelled to get one of those capsules.

The discs pause their motion each second and come in different sizes;
they seem to each have a fixed number of positions at which they stop.
You decide to call the position with the slot 0,
and count up for each position it reaches next.

Furthermore, the discs are spaced out so that after you push the button,
one second elapses before the first disc is reached,
and one second elapses as the capsule passes from one disc to the one below it.
So, if you push the button at time=100,
then the capsule reaches the top disc at time=101,
the second disc at time=102, the third disc at time=103, and so on.

The button will only drop a capsule at an integer time - no fractional seconds allowed.

For example, at time=0, suppose you see the following arrangement:

- Disc #1 has 5 positions; at time=0, it is at position 4.
- Disc #2 has 2 positions; at time=0, it is at position 1.

If you press the button exactly at time=0, the capsule would start to fall;
it would reach the first disc at time=1.
Since the first disc was at position 4 at time=0,
by time=1 it has ticked one position forward.
As a five-position disc, the next position is 0, and the capsule falls through the slot.

Then, at time=2, the capsule reaches the second disc.
The second disc has ticked forward two positions at this point:
it started at position 1, then continued to position 0,
and finally ended up at position 1 again.
Because there's only a slot at position 0, the capsule bounces away.

If, however, you wait until time=5 to push the button,
then when the capsule reaches each disc,
the first disc will have ticked forward 5+1 = 6 times (to position 0),
and the second disc will have ticked forward 5+2 = 7 times (also to position 0).
In this case, the capsule would fall through the discs and come out of the machine.

However, your situation has more than two discs;
you've noted their positions in your puzzle input.
What is the first time you can press the button to get a capsule?
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
    print(solve(discs))
