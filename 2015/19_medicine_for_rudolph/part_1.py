"""
Rudolph the Red-Nosed Reindeer is sick! His nose isn't shining very brightly,
and he needs medicine.

Red-Nosed Reindeer biology isn't similar to regular reindeer biology;
Rudolph is going to need custom-made medicine.
Unfortunately, Red-Nosed Reindeer chemistry
isn't similar to regular reindeer chemistry, either.

The North Pole is equipped with a Red-Nosed Reindeer nuclear fusion/fission plant,
capable of constructing any Red-Nosed Reindeer molecule you need.
It works by starting with some input molecule and then doing a series of replacements,
one per step, until it has the right molecule.

However, the machine has to be calibrated before it can be used.
Calibration involves determining the number of molecules
that can be generated in one step from a given starting point.

For example, imagine a simpler machine that supports only the following replacements:

- H => HO
- H => OH
- O => HH

Given the replacements above and starting with HOH,
the following molecules could be generated:

- HOOH (via H => HO on the first H).
- HOHO (via H => HO on the second H).
- OHOH (via H => OH on the first H).
- HOOH (via H => OH on the second H).
- HHHH (via O => HH).

So, in the example above, there are 4 distinct molecules
(not five, because HOOH appears twice) after one replacement from HOH.
Santa's favorite molecule, HOHOHO, can become 7 distinct molecules
(over nine replacements: six from H, and three from O).

The machine replaces without regard for the surrounding characters.
For example, given the string H2O, the transition H => OO would result in OO2O.

How many distinct molecules can be created
after all the different ways you can do one replacement on the medicine molecule?
"""

from collections.abc import Iterator
from itertools import chain

from parse import parse


def calibrate(molecule: str, replacements: list[tuple[str, str]]) -> set[str]:
    new_molecules = (
        _build_new_molecules(molecule, from_, to_) for from_, to_ in replacements
    )
    return set(chain.from_iterable(new_molecules))


def _build_new_molecules(molecule, from_, to_) -> Iterator[str]:
    start = 0

    while (pos := molecule.find(from_, start)) >= 0:
        yield molecule[:pos] + to_ + molecule[pos + len(from_) :]
        start = pos + 1


assert list(_build_new_molecules("A", "A", "B")) == ["B"]
assert list(_build_new_molecules("AA", "A", "B")) == ["BA", "AB"]
assert list(_build_new_molecules("C", "A", "B")) == []

replacements = [("H", "HO"), ("H", "OH"), ("O", "HH")]
assert calibrate("HOH", replacements) == {"HOOH", "HOHO", "OHOH", "HHHH"}


with open("2015/19_medicine_for_rudolph/replacements.txt") as f:
    spec = "{} => {}"
    replacements = [parse(spec, line.strip()).fixed for line in f]

with open("2015/19_medicine_for_rudolph/molecule.txt") as f:
    molecule = f.read()

print(len(calibrate(molecule, replacements)))
