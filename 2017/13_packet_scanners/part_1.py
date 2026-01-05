"""
You need to cross a vast firewall. The firewall consists of several layers,
each with a security scanner that moves back and forth across the layer.
To succeed, you must not be detected by a scanner.

By studying the firewall briefly,
you are able to record (in your puzzle input) the depth of each layer
and the range of the scanning area for the scanner within it, written as depth: range.
Each layer has a thickness of exactly 1.
A layer at depth 0 begins immediately inside the firewall;
a layer at depth 1 would start immediately after that.

For example, suppose you've recorded the following:

0: 3
1: 2
4: 4
6: 4

This means that there is a layer immediately inside the firewall (with range 3),
a second layer immediately after that (with range 2),
a third layer which begins at depth 4 (with range 4),
and a fourth layer which begins at depth 6 (also with range 4).
Visually, it might look like this:

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Within each layer, a security scanner moves back and forth within its range.
Each security scanner starts at the top and moves down until it reaches the bottom,
then moves up until it reaches the top, and repeats.
A security scanner takes one picosecond to move one step.
Drawing scanners as S, the first few picoseconds look like this:


Picosecond 0:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 1:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

Your plan is to hitch a ride on a packet about to move through the firewall.
The packet will travel along the top of each layer,
and it moves at one layer per picosecond.
Each picosecond, the packet moves one layer forward
(its first move takes it into layer 0), and then the scanners move one step.
If there is a scanner at the top of the layer as your packet enters it, you are caught.
(If a scanner moves into the top of its layer while you are there, you are not caught:
it doesn't have time to notice you before you leave.)
If you were to do this in the configuration above,
marking your current position with parentheses,
your passage through the firewall would look like this:

Initial state:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 0:
 0   1   2   3   4   5   6
(S) [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 1:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] (S) ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]


Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] (.) ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]


Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]


Picosecond 4:
 0   1   2   3   4   5   6
[S] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 5:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... ... [S] (.) [S]
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]


Picosecond 6:
 0   1   2   3   4   5   6
[ ] [S] ... ... [S] ... (S)
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

In this situation, you are caught in layers 0 and 6, because
your packet entered the layer when its scanner was at the top when you entered it.
You are not caught in layer 1,
since the scanner moved into the top of the layer once you were already there.

The severity of getting caught on a layer is equal to its depth multiplied by its range.
(Ignore layers in which you do not get caught.)
The severity of the whole trip is the sum of these values.
In the example above, the trip severity is 0*3 + 6*4 = 24.

Given the details of the firewall you've recorded, if you leave immediately,
what is the severity of your whole trip?
"""

from enum import StrEnum, auto
from typing import NamedTuple

from parse import parse

type Firewall = list[Layer]


class Direction(StrEnum):
    FORWARD = auto()
    BACKWARD = auto()


class Layer(NamedTuple):
    index: int
    depth: int


def get_trip_severity(raw_firewall: list[str]) -> int:
    firewall = map(_parse_layer, raw_firewall)
    severity = 0

    for layer in firewall:
        pos = _get_scanner_pos(layer.index, layer.depth)

        match pos:
            case Direction.FORWARD, 1:
                severity += layer.index * layer.depth
            case _:
                continue

    return severity


def _get_scanner_pos(tick: int, depth: int) -> tuple[Direction, int] | None:
    if depth == 0:
        return None

    pos = 0
    direction = Direction.FORWARD

    for _ in range(tick + 1):
        if pos == depth - 1:
            direction = Direction.BACKWARD
        elif pos == 0:
            direction = Direction.FORWARD

        pos += 1 if direction == Direction.FORWARD else -1

    return direction, pos


def _parse_layer(raw_layer: str) -> Layer:
    return Layer(*parse("{:d}: {:d}", raw_layer).fixed)


assert _parse_layer("0: 3") == Layer(0, 3)

assert _get_scanner_pos(0, 2) == (Direction.FORWARD, 1)
assert _get_scanner_pos(1, 2) == (Direction.BACKWARD, 0)
assert _get_scanner_pos(2, 2) == (Direction.FORWARD, 1)
assert _get_scanner_pos(3, 2) == (Direction.BACKWARD, 0)

assert _get_scanner_pos(0, 4) == (Direction.FORWARD, 1)
assert _get_scanner_pos(1, 4) == (Direction.FORWARD, 2)
assert _get_scanner_pos(2, 4) == (Direction.FORWARD, 3)
assert _get_scanner_pos(3, 4) == (Direction.BACKWARD, 2)
assert _get_scanner_pos(4, 4) == (Direction.BACKWARD, 1)
assert _get_scanner_pos(5, 4) == (Direction.BACKWARD, 0)
assert _get_scanner_pos(6, 4) == (Direction.FORWARD, 1)


firewall = [
    "0: 3",
    "1: 2",
    "4: 4",
    "6: 4",
]
assert get_trip_severity(firewall) == 24


with open("2017/13_packet_scanners/input.txt") as f:
    lines = [line.strip() for line in f]
    print(get_trip_severity(lines))
