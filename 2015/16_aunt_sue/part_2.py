"""
As you're about to send the thank you note,
something in the MFCSAM's instructions catches your eye.
Apparently, it has an outdated retroencabulator,
and so the output from the machine isn't exact values - some of them indicate ranges.

In particular, the cats and trees readings indicates
that there are greater than that many
(due to the unpredictable nuclear decay of cat dander and tree pollen),
while the pomeranians and goldfish readings indicate
that there are fewer than that many
(due to the modial interaction of magnetoreluctance).

What is the number of the real Aunt Sue?
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
        if v is None or aunt_value is None:
            continue
        if not _match_prop(k, value=aunt_value, target_value=v):
            return False
    return True


def _match_prop(prop, *, value, target_value) -> bool:
    if prop in {"cats", "trees"}:
        return value > target_value

    if prop in {"pomeranians", "goldfish"}:
        return value < target_value

    return value == target_value


target = Aunt(cats=1)
aunts = [Aunt(children=1), Aunt(cats=2)]
assert find_aunt(aunts, target) == (1, aunts[0])

target = Aunt(cats=1, trees=1)
aunts = [Aunt(children=1), Aunt(cats=2)]
assert find_aunt(aunts, target) == (1, aunts[0])

target = Aunt(cats=1, trees=1)
aunts = [Aunt(children=1, cats=2), Aunt(cats=1)]
assert find_aunt(aunts, target) == (1, aunts[0])

target = Aunt(cats=1, trees=1)
aunts = [Aunt(cats=2), Aunt(cats=1)]
assert find_aunt(aunts, target) == (1, aunts[0])

target = Aunt(goldfish=2)
aunts = [Aunt(goldfish=2), Aunt(goldfish=1)]
assert find_aunt(aunts, target) == (2, aunts[1])

target = Aunt(children=2)
aunts = [Aunt(children=1), Aunt(children=2)]
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
