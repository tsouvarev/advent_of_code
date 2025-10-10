"""
Finally, you come across an information kiosk with a list of rooms.
Of course, the list is encrypted and full of decoy data,
but the instructions to decode the list are barely hidden nearby.
Better remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by dashes)
followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy)
if the checksum is the five most common letters in the encrypted name, in order,
with ties broken by alphabetization. For example:

-   aaaaa-bbb-z-y-x-123[abxyz] is a real room
    because the most common letters are a (5), b (3),
    and then a tie between x, y, and z, which are listed alphabetically.
-   a-b-c-d-e-f-g-h-987[abcde] is a real room
    because although the letters are all tied (1 of each),
    the first five are listed alphabetically.
-   not-a-real-room-404[oarel] is a real room.
-   totally-real-room-200[decoy] is not.

Of the real rooms from the list above, the sum of their sector IDs is 1514.

What is the sum of the sector IDs of the real rooms?
"""

from collections import Counter
from typing import NamedTuple

from parse import parse


class Room(NamedTuple):
    name: str
    sector_id: int
    checksum: str


def is_real_room(room: Room) -> bool:
    return _get_checksum(room.name) == room.checksum


def _get_checksum(name: str) -> str:
    # can't use most_common because of custom logic of ties
    most_common_letters = Counter(name).items()
    sorted_alphabetically = sorted(
        most_common_letters,
        reverse=True,
        key=_break_ties_with_alphabetization,
    )
    return "".join(k for k, _ in sorted_alphabetically).replace("-", "")[:5]


def _break_ties_with_alphabetization(el: tuple[str, int]) -> tuple[int, int]:
    return el[1], -ord(el[0])


def _parse(s: str) -> Room:
    return Room(*parse("{:D}-{:d}[{:w}]", s).fixed)


assert _parse("aaaaa-bbb-z-y-x-123[abxyz]") == Room("aaaaa-bbb-z-y-x", 123, "abxyz")

assert _get_checksum("aaaaabbbzyx") == "abxyz"
assert _get_checksum("abcdefgh") == "abcde"
assert _get_checksum("notarealroom") == "oarel"

assert is_real_room(_parse("aaaaa-bbb-z-y-x-123[abxyz]")) is True
assert is_real_room(_parse("a-b-c-d-e-f-g-h-987[abcde]")) is True
assert is_real_room(_parse("not-a-real-room-404[oarel]")) is True
assert is_real_room(_parse("totally-real-room-200[decoy]")) is False


with open("2016/04_security_through_obscurity/input.txt") as f:
    res = 0

    for line in f:
        room = _parse(line.strip())
        if is_real_room(room):
            res += room.sector_id

    print(res)
