"""
Realizing the folly of their present-exchange rules,
the Elves agree to instead steal presents from the Elf directly across the circle.
If two Elves are across the circle,
the one on the left (from the perspective of the stealer) is stolen from.
The other rules remain unchanged:
Elves with no presents are removed from the circle entirely,
and the other elves move in slightly to keep the circle evenly spaced.

For example, with five Elves (again numbered 1 to 5):

The Elves sit in a circle; Elf 1 goes first:

  1
5   2
 4 3

Elves 3 and 4 are across the circle;
Elf 3's present is stolen, being the one to the left.
Elf 3 leaves the circle, and the rest of the Elves move in:

  1           1
5   2  -->  5   2
 4 -          4

Elf 2 steals from the Elf directly across the circle, Elf 5:

  1         1
-   2  -->     2
  4         4

Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:

 -          2
    2  -->
 4          4

Finally, Elf 2 steals from Elf 4:

 2
    -->  2
 -

So, with five Elves, the Elf that sits starting in position 2 gets all the presents.

With the number of Elves given in your puzzle input,
which Elf now gets all the presents?
"""

from collections import deque
from dataclasses import dataclass

type Party = list[Elf]


@dataclass(kw_only=True)
class Elf:
    pos: int
    n: int


def solve(num_elves: int) -> int:
    party = _gen_party(num_elves)
    half = num_elves // 2 + 1
    left, right = deque(party[:half]), deque(party[half:])

    while left and right:
        victim = left.pop() if len(left) > len(right) else right.popleft()

        thief = left.popleft()
        thief.n += victim.n

        right.append(thief)
        left.append(right.popleft())

    return (left or right)[0].pos


def _gen_party(n: int) -> Party:
    return [Elf(pos=i, n=1) for i in range(1, n + 1)]


def _steal(thief, victim) -> Elf:
    thief.n += victim.n
    return thief


def _get_opposite_elf(n: int) -> int:
    return n // 2


assert _get_opposite_elf(1) == 0
"""
  1
  2
"""
assert _get_opposite_elf(2) == 1
"""
  1
 3 2
"""
assert _get_opposite_elf(3) == 1
"""
  1
 4 2
  3
"""
assert _get_opposite_elf(4) == 2
"""
  1
5   2
 4 3
"""
assert _get_opposite_elf(5) == 2


assert solve(1) == 1
assert solve(2) == 1
assert solve(3) == 3
assert solve(4) == 1
assert solve(5) == 2

print(solve(3_014_603))
