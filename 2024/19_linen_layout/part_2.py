"""
The staff don't really like some of the towel arrangements you came up with.
To avoid an endless cycle of towel rearrangement,
maybe you should just give them every possible option.

Here are all of the different ways the above example's designs can be made:

brwrr can be made in two different ways: b, r, wr, r or br, wr, r.
bggr can only be made with b, g, g, and r.
gbbr can be made 4 different ways:
    g, b, b, r
    g, b, br
    gb, b, r
    gb, br
rrbgbr can be made 6 different ways:
    r, r, b, g, b, r
    r, r, b, g, br
    r, r, b, gb, r
    r, rb, g, b, r
    r, rb, g, br
    r, rb, gb, r
bwurrg can only be made with bwu, r, r, and g.
brgr can be made in two different ways: b, r, g, r or br, g, r.
ubwu and bbrgwb are still impossible.

Adding up all of the ways the towels in this example
could be arranged into the desired designs yields 16 (2 + 1 + 4 + 6 + 1 + 2).

They'll let you into the onsen as soon as you have the list.
What do you get if you add up the number of different ways you could make each design?
"""

from functools import cache

type Design = str
type Towel = str


@cache
def count_combos(towels: tuple[Towel, ...], design: Design) -> set[list[str]]:
    combos = 0
    for towel in towels:
        if design.startswith(towel):
            if towel == design:
                combos += 1
            else:
                other_combos = count_combos(towels, design.removeprefix(towel))
                combos += other_combos

    return combos


towels = ("r", "wr", "b", "g", "bwu", "rb", "gb", "br")
assert count_combos(towels, "brwrr") == 2
assert count_combos(towels, "bggr") == 1
assert count_combos(towels, "gbbr") == 4
assert count_combos(towels, "rrbgbr") == 6
assert count_combos(towels, "ubwu") == 0
assert count_combos(towels, "bwurrg") == 1
assert count_combos(towels, "brgr") == 2
assert count_combos(towels, "bbrgwb") == 0

with open("2024/19_linen_layout/input_towels.txt") as f:
    towels = tuple(f.read().split(", "))

with open("2024/19_linen_layout/input_designs.txt") as f:
    designs = f.read().splitlines()

print(sum(count_combos(towels, d) for d in designs))
