"""
The Elves contact you over a highly secure emergency channel.
Back at the North Pole, the Elves are busy misunderstanding White Elephant parties.

Each Elf brings a present. They all sit in a circle, numbered starting with position 1.
Then, starting with the first Elf, they take turns
stealing all the presents from the Elf to their left.
An Elf with no presents is removed from the circle and does not take turns.

For example, with five Elves (numbered 1 to 5):

  1
5   2
 4 3

- Elf 1 takes Elf 2's present.
- Elf 2 has no presents and is skipped.
- Elf 3 takes Elf 4's present.
- Elf 4 has no presents and is also skipped.
- Elf 5 takes Elf 1's two presents.
- Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
- Elf 3 takes Elf 5's three presents.

So, with five Elves, the Elf that sits starting in position 3 gets all the presents.

With the number of Elves given in your puzzle input, which Elf gets all the presents?
"""

from dataclasses import dataclass
from itertools import batched, chain

type Party = list[Elf]


@dataclass(kw_only=True)
class Elf:
    pos: int
    n: int


def solve(num_elves: int) -> int:
    party = _gen_party(num_elves)

    while len(party) > 1:
        party = _steal_presents(party)

    return party[0].pos


def _gen_party(n: int) -> Party:
    return [Elf(pos=i, n=1) for i in range(1, n + 1)]


def _steal_presents(party: Party) -> Party:
    print(len(party))

    if len(party) % 2 == 1:
        # last elf will steal from first two elves
        party = chain(  # type: ignore[invalid-assignment]
            party[2:],
            [_steal(*party[:2])],
        )

    return [_steal(*elves) for elves in batched(party, 2)]


def _steal(thief, victim) -> Elf:
    thief.n += victim.n
    return thief


assert list(_steal_presents(_gen_party(3))) == [Elf(pos=3, n=3)]
assert list(_steal_presents(_gen_party(4))) == [Elf(pos=1, n=2), Elf(pos=3, n=2)]
assert list(_steal_presents(_gen_party(5))) == [Elf(pos=3, n=2), Elf(pos=5, n=3)]


assert solve(1) == 1
assert solve(2) == 1
assert solve(3) == 3
assert solve(4) == 1
assert solve(5) == 3

print(solve(3_014_603))
