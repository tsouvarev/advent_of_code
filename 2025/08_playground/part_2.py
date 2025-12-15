"""
The Elves were right; they definitely don't have enough extension cables.
You'll need to keep connecting junction boxes together
until they're all in one large circuit.

Continuing the above example,
the first connection which causes all of the junction boxes to form a single circuit
is between the junction boxes at 216,146,977 and 117,168,530.
The Elves need to know how far those junction boxes
are from the wall so they can pick the right extension cable;
multiplying the X coordinates of those two junction boxes (216 and 117) produces 25272.

Continue connecting the closest unconnected pairs of junction boxes together
until they're all in the same circuit.
What do you get if you multiply together
the X coordinates of the last two junction boxes you need to connect?
"""

from collections.abc import Iterable
from itertools import combinations
from typing import NamedTuple

from parse import parse

type Pair = tuple[Box, Box]


class Box(NamedTuple):
    x: int
    y: int
    z: int


def connect(boxes: list[Box]):
    pairs = _sort_by_distance(boxes)
    map_box_to_circuit = {box: {box} for box in boxes}

    for box_1, box_2 in pairs:
        circuit_1 = map_box_to_circuit[box_1]
        circuit_2 = map_box_to_circuit[box_2]

        joined_circuit = circuit_1 | circuit_2
        if len(joined_circuit) == len(boxes):
            break

        for box in joined_circuit:
            map_box_to_circuit[box] = joined_circuit

    return box_1.x * box_2.x


def _sort_by_distance(boxes: list[Box]) -> Iterable[Pair]:
    distances = ((_get_distance(*pair), pair) for pair in combinations(boxes, 2))
    for _, pair in sorted(distances):
        yield pair


def _get_distance(p1: Box, p2: Box) -> int:
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2


boxes = [
    Box(162, 817, 812),
    Box(57, 618, 57),
    Box(906, 360, 560),
    Box(592, 479, 940),
    Box(352, 342, 300),
    Box(466, 668, 158),
    Box(542, 29, 236),
    Box(431, 825, 988),
    Box(739, 650, 466),
    Box(52, 470, 668),
    Box(216, 146, 977),
    Box(819, 987, 18),
    Box(117, 168, 530),
    Box(805, 96, 715),
    Box(346, 949, 466),
    Box(970, 615, 88),
    Box(941, 993, 340),
    Box(862, 61, 35),
    Box(984, 92, 344),
    Box(425, 690, 689),
]
assert connect(boxes) == 25272

with open("2025/08_playground/input.txt") as f:
    boxes = [Box(*parse("{:d},{:d},{:d}", line.strip()).fixed) for line in f]
    print(connect(boxes))
