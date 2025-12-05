"""
The clerk quickly discovers that there are still invalid IDs in the ranges in your list.
Maybe the young Elf was doing other silly patterns as well?

Now, an ID is invalid
if it is made only of some sequence of digits repeated at least twice.
So, 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times),
and 1111111 (1 seven times) are all invalid IDs.

From the same example as before:

- 11-22 still has two invalid IDs, 11 and 22.
- 95-115 now has two invalid IDs, 99 and 111.
- 998-1012 now has two invalid IDs, 999 and 1010.
- 1188511880-1188511890 still has one invalid ID, 1188511885.
- 222220-222224 still has one invalid ID, 222222.
- 1698522-1698528 still contains no invalid IDs.
- 446443-446449 still has one invalid ID, 446446.
- 38593856-38593862 still has one invalid ID, 38593859.
- 565653-565659 now has one invalid ID, 565656.
- 824824821-824824827 now has one invalid ID, 824824824.
- 2121212118-2121212124 now has one invalid ID, 2121212121.

Adding up all the invalid IDs in this example produces 4174379265.

What do you get if you add up all of the invalid IDs using these new rules?
"""

import re
from collections.abc import Iterator
from typing import NamedTuple


class GiftRange(NamedTuple):
    start: int
    end: int


def get_invalid_gift_ids(ranges: str) -> Iterator[int]:
    for gift_range in _parse_ranges(ranges):
        for gift_id in _gen_gift_ids(gift_range):
            if not _is_valid(gift_id):
                yield gift_id


def _is_valid(gift_id: int) -> bool:
    return re.fullmatch(r"(\d+)\1+", str(gift_id)) is None


def _gen_gift_ids(gift_range: GiftRange) -> Iterator[int]:
    yield from range(gift_range.start, gift_range.end + 1)


def _parse_ranges(raw_ranges: str) -> list[GiftRange]:
    return [
        GiftRange(*map(int, raw_range.split("-")))
        for raw_range in raw_ranges.split(",")
    ]


assert _is_valid(11) is False
assert _is_valid(121) is True
assert _is_valid(123123123) is False

assert _parse_ranges("11-22,95-115") == [GiftRange(11, 22), GiftRange(95, 115)]

assert list(_gen_gift_ids(GiftRange(1, 2))) == [1, 2]

assert list(get_invalid_gift_ids("11-22")) == [11, 22]
assert list(get_invalid_gift_ids("95-115")) == [99, 111]

with open("2025/02_gift_shop/input.txt") as f:
    print(sum(get_invalid_gift_ids(f.read().strip())))
