"""
Your Aunt Sue has given you a wonderful gift,
and you'd like to send her a thank you card.
However, there's a small problem: she signed it "From, Aunt Sue".

You have 500 Aunts named "Sue".

So, to avoid sending the card to the wrong person,
you need to figure out which Aunt Sue
(which you conveniently number 1 to 500, for sanity) gave you the gift.
You open the present and, as luck would have it, good ol' Aunt Sue got you
a My First Crime Scene Analysis Machine! Just what you wanted.
Or needed, as the case may be.

The My First Crime Scene Analysis Machine (MFCSAM for short)
can detect a few specific compounds in a given sample,
as well as how many distinct kinds of those compounds there are.
According to the instructions, these are what the MFCSAM can detect:

- children, by human DNA age analysis.
- cats. It doesn't differentiate individual breeds.
- Several seemingly random breeds of dog: samoyeds, pomeranians, akitas, and vizslas.
- goldfish. No other kinds of fish.
- trees, all in one group.
- cars, presumably by exhaust or gasoline or something.
- perfumes, which is handy, since many of your Aunts Sue wear a few kinds.

In fact, many of your Aunts Sue have many of these.
You put the wrapping from the gift into the MFCSAM.
It beeps inquisitively at you a few times and then prints out a message on ticker tape:

children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1

You make a list of the things you can remember about each Aunt Sue.
Things missing from your list aren't zero - you simply don't remember the value.

What is the number of the Sue that got you the gift?
"""

from dataclasses import dataclass
from itertools import batched

from parse import parse


@dataclass(kw_only=True)
class Aunt:
    children: int | None = None
    cats: int | None = None
    samoyeds: int | None = None
    pomeranians: int | None = None
    akitas: int | None = None
    vizslas: int | None = None
    goldfish: int | None = None
    trees: int | None = None
    cars: int | None = None
    perfumes: int | None = None


def find_aunt(aunts: list[Aunt], target: Aunt) -> tuple[int, Aunt]:
    for i, aunt in enumerate(aunts, 1):
        if _match_aunt(aunt, target):
            return i, aunt
    return None


def _match_aunt(aunt: Aunt, target: Aunt) -> bool:
    for k, v in target.__dict__.items():
        aunt_value = getattr(aunt, k)
        if v is None or aunt_value is None or aunt_value == v:
            continue
        return False

    return True


target = Aunt(cats=1)
aunts = [Aunt(children=1), Aunt(cats=1)]
assert find_aunt(aunts, target) == (1, aunts[0])

target = Aunt(cats=1, trees=1)
aunts = [Aunt(children=1), Aunt(cats=1)]
assert find_aunt(aunts, target) == (1, aunts[0])

target = Aunt(cats=1, trees=1)
aunts = [Aunt(children=1, cats=2), Aunt(cats=1)]
assert find_aunt(aunts, target) == (2, aunts[1])


target = Aunt(
    children=3,
    cats=7,
    samoyeds=2,
    pomeranians=3,
    akitas=0,
    vizslas=0,
    goldfish=5,
    trees=3,
    cars=2,
    perfumes=1,
)
with open("2015/16_aunt_sue/input.txt") as f:
    spec = "Sue {}: {}: {:d}, {}: {:d}, {}: {:d}"
    aunts = [
        Aunt(**dict(batched(parse(spec, line.strip()).fixed[1:], n=2))) for line in f
    ]

    print(find_aunt(aunts, target))
