"""
With all the decoy data out of the way, it's time to decrypt this list and get moving.

The room names are encrypted by a state-of-the-art shift cipher,
which is nearly unbreakable without the right software.
However, the information kiosk designers at Easter Bunny HQ were not expecting
to deal with a master cryptographer like yourself.

To decrypt a room name, rotate each letter forward through the alphabet
a number of times equal to the room's sector ID.
A becomes B, B becomes C, Z becomes A, and so on. Dashes become spaces.

For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.

What is the sector ID of the room where North Pole objects are stored?
"""

import string
from itertools import cycle, islice
from typing import NamedTuple

from parse import parse


class Room(NamedTuple):
    name: str
    sector_id: int
    checksum: str


def decrypt_room(s: str) -> str:
    room = _parse(s)
    return "".join(_rotate_letter(l, room.sector_id) for l in room.name)


def _rotate_letter(l: str, n: int) -> str:
    if l == "-":
        return " "

    base = ord(l) - ord("a")
    offset = base + n
    letters = cycle(string.ascii_lowercase)
    return next(islice(letters, offset, offset + 1))


def _parse(s: str) -> Room:
    return Room(*parse("{:D}-{:d}[{:w}]", s).fixed)


assert _parse("aaaaa-bbb-z-y-x-123[abxyz]") == Room("aaaaa-bbb-z-y-x", 123, "abxyz")

assert _rotate_letter("-", 1) == " "
assert _rotate_letter("a", 1) == "b"

assert decrypt_room("qzmt-zixmtkozy-ivhz-343[a]") == "very encrypted name"


with open("2016/04_security_through_obscurity/input.txt") as f:
    res = 0

    for line in f:
        decrypted = decrypt_room(line.strip())
        if "north" in decrypted.lower():
            print(line, decrypted)
