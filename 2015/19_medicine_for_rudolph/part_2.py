"""
Now that the machine is calibrated, you're ready to begin molecule fabrication.

Molecule fabrication always begins with just a single electron, e,
and applying replacements one at a time, just like the ones during calibration.

For example, suppose you have the following replacements:

e => H
e => O
H => HO
H => OH
O => HH

If you'd like to make HOH, you start with e, and then make the following replacements:

    e => O to get O
    O => HH to get HH
    H => OH (on the second H) to get HOH

So, you could make HOH after 3 steps.
Santa's favorite molecule, HOHOHO, can be made in 6 steps.

How long will it take to make the medicine?
Given the available replacements and the medicine molecule in your puzzle input,
what is the fewest number of steps to go from e to the medicine molecule?
"""

from parse import parse


def reduce_molecule(
    molecule: str,
    replacements: list[tuple[str, str]],
    history: list[str] | None = None,
) -> list[list[str]]:
    if history is None:
        history = []
    if molecule == "e":
        return [history]

    histories = []
    for from_, to_ in replacements:
        if to_ in molecule:
            reduced_molecule = _build_new_molecule(molecule, from_, to_)
            res = reduce_molecule(
                reduced_molecule,
                replacements,
                [*history, (to_, from_)],
            )
            if res:
                histories.extend(res)

    return histories


def _build_new_molecule(molecule, from_, to_) -> str:
    pos = molecule.find(to_)
    return molecule[:pos] + from_ + molecule[pos + len(to_) :]


replacements = [("e", "H")]
assert reduce_molecule("H", replacements) == [[("H", "e")]]

replacements = [("e", "H"), ("H", "O")]
assert reduce_molecule("O", replacements) == [[("O", "H"), ("H", "e")]]

replacements = [("e", "H"), ("e", "O"), ("H", "HO"), ("H", "OH"), ("O", "HH")]
assert reduce_molecule("HOH", replacements) == [
    [("HO", "H"), ("HH", "O"), ("O", "e")],
    [("OH", "H"), ("HH", "O"), ("O", "e")],
]


with open("2015/19_medicine_for_rudolph/replacements.txt") as f:
    spec = "{} => {}"
    replacements = [parse(spec, line.strip()).fixed for line in f]

with open("2015/19_medicine_for_rudolph/molecule.txt") as f:
    molecule = f.read()

print(reduce_molecule(molecule, replacements))
