"""
The Elves start bringing their spoiled inventory to the trash chute
at the back of the kitchen.

So that they can stop bugging you when they get new inventory,
the Elves would like to know
all of the IDs that the fresh ingredient ID ranges consider to be fresh.
An ingredient ID is still considered fresh if it is in any range.

Now, the second section of the database (the available ingredient IDs) is irrelevant.
Here are the fresh ingredient ID ranges from the above example:

3-5
10-14
16-20
12-18

The ingredient IDs that these ranges consider to be fresh
are 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20.
So, in this example, the fresh ingredient ID ranges consider
a total of 14 ingredient IDs to be fresh.

Process the database file again.
How many ingredient IDs are considered to be fresh
according to the fresh ingredient ID ranges?
"""

from collections.abc import Iterable
from typing import NamedTuple


class Range(NamedTuple):
    start: int
    end: int


def len_fresh_ingredients(raw_ranges: list[str]) -> int:
    ranges = map(_parse_range, raw_ranges)
    ranges = _collapse_ranges(ranges)

    res = 0
    for range_ in ranges:
        res += range_.end - range_.start + 1

    return res


def _collapse_ranges(ranges: Iterable[Range]) -> list[Range]:
    res = []
    ranges = sorted(ranges)
    start, end = ranges[0]

    for range_ in ranges[1:]:
        if range_.start > end:
            res.append(Range(start, end))
            start, end = range_
        else:
            end = max(end, range_.end)

    res.append(Range(start, end))

    return res


def _parse_range(raw_range: str) -> Range:
    return Range(*map(int, raw_range.split("-")))


assert _collapse_ranges([Range(3, 5), Range(10, 14)]) == [Range(3, 5), Range(10, 14)]
assert _collapse_ranges([Range(3, 5), Range(4, 7)]) == [Range(3, 7)]
assert _collapse_ranges([Range(3, 10), Range(4, 7)]) == [Range(3, 10)]

assert len_fresh_ingredients(["3-5", "10-14"]) == 8
assert len_fresh_ingredients(["3-5", "4-7"]) == 5
assert len_fresh_ingredients(["3-5", "10-14", "16-20", "12-18"]) == 14


with open("2025/05_cafeteria/input_ranges.txt") as f:
    ranges = [line.strip() for line in f]

print(len_fresh_ingredients(ranges))
