"""
Apparently, the file actually uses version two of the format.

In version two, the only difference
is that markers within decompressed data are decompressed.
This, the documentation explains,
provides much more substantial compression capabilities,
allowing many-gigabyte files to be stored in only a few kilobytes.

For example:

-   (3x3)XYZ still becomes XYZXYZXYZ, as the decompressed section contains no markers.
-   X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY,
    because the decompressed data from the (8x2) marker is then further decompressed,
    thus triggering the (3x3) marker twice for a total of six ABC sequences.
-   (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into
    a string of A repeated 241920 times.
-   (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN
    becomes 445 characters long.

Unfortunately, the computer you brought probably doesn't have enough memory
to actually decompress the file;
you'll have to come up with another way to get its decompressed length.

What is the decompressed length of the file using this improved format?
"""

from collections.abc import Iterable
from itertools import islice, takewhile
from typing import NamedTuple

from parse import parse


class Marker(NamedTuple):
    length: int
    n: int


def decompress(s: Iterable[str]) -> int:
    s_iter = iter(s)
    res = 0

    while True:
        c = next(s_iter, None)

        if c is None:
            break
        if c == "(":
            marker = _collect_marker(s_iter)
            subseq_len = decompress(islice(s_iter, marker.length))
            res += subseq_len * marker.n
        else:
            res += 1

    return res


def _collect_marker(s: str) -> Marker:
    raw_marker = "".join(takewhile(lambda c: c != ")", s))
    marker_parts = parse("{:d}x{:d}", raw_marker).fixed
    return Marker(*marker_parts)


assert decompress("(3x3)XYZ") == 9
assert decompress("X(8x2)(3x3)ABCY") == 20
assert decompress("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920
assert decompress("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445


with open("2016/09_explosives_in_cyberspace/input.txt") as f:
    print(decompress(f.read().strip()))
