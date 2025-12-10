"""
As the forklifts break through the wall,
the Elves are delighted to discover that
there was a cafeteria on the other side after all.

You can hear a commotion coming from the kitchen.
"At this rate, we won't have any time left to put the wreaths up in the dining hall!"
Resolute in your quest, you investigate.

"If only we hadn't switched to the new inventory management system
right before Christmas!" another Elf exclaims. You ask what's going on.

The Elves in the kitchen explain the situation:
because of their complicated new inventory management system,
they can't figure out which of their ingredients are fresh and which are spoiled.
When you ask how it works, they give you a copy of their database (your puzzle input).

The database operates on ingredient IDs.
It consists of a list of fresh ingredient ID ranges, a blank line,
and a list of available ingredient IDs. For example:

3-5
10-14
16-20
12-18

1
5
8
11
17
32

The fresh ID ranges are inclusive: the range 3-5 means
that ingredient IDs 3, 4, and 5 are all fresh.
The ranges can also overlap; an ingredient ID is fresh if it is in any range.

The Elves are trying to determine which of the available ingredient IDs are fresh.
In this example, this is done as follows:

- Ingredient ID 1 is spoiled because it does not fall into any range.
- Ingredient ID 5 is fresh because it falls into range 3-5.
- Ingredient ID 8 is spoiled.
- Ingredient ID 11 is fresh because it falls into range 10-14.
- Ingredient ID 17 is fresh because it falls into range 16-20 as well as range 12-18.
- Ingredient ID 32 is spoiled.

So, in this example, 3 of the available ingredient IDs are fresh.

Process the database file from the new inventory management system.
How many of the available ingredient IDs are fresh?
"""

from typing import NamedTuple


class Range(NamedTuple):
    start: int
    end: int


def get_fresh_ingredients(ranges: list[Range], available_ids: list[int]) -> list[int]:
    res = []

    for id_ in available_ids:
        for fresh_range in ranges:
            if _is_in_range(id_, fresh_range):
                res.append(id_)
                break

    return res


def _is_in_range(id_: int, fresh_range: Range) -> bool:
    return fresh_range.start <= id_ <= fresh_range.end


def _parse_range(raw_range: str) -> Range:
    return Range(*map(int, raw_range.split("-")))


ranges = list(map(_parse_range, ["3-5", "10-14", "16-20", "12-18"]))
ids = [1, 5, 8, 11, 17, 32]
assert get_fresh_ingredients(ranges, ids) == [5, 11, 17]


with open("2025/05_cafeteria/input_ranges.txt") as f:
    ranges = []
    for line in f:
        ranges.append(_parse_range(line.strip()))

with open("2025/05_cafeteria/input_ids.txt") as f:
    ids = []
    for line in f:
        ids.append(int(line.strip()))

print(len(get_fresh_ingredients(ranges, ids)))
