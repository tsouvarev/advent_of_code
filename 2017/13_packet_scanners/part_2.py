"""
Now, you need to pass through the firewall without being caught - easier said than done.

You can't control the speed of the packet,
but you can delay it any number of picoseconds.
For each picosecond you delay the packet before beginning your trip,
all security scanners move one step.
You're not in the firewall during this time;
you don't enter layer 0 until you stop delaying the packet.

In the example above, if you delay 10 picoseconds (picoseconds 0 - 9),
you won't get caught:

State after delaying:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 10:
 0   1   2   3   4   5   6
( ) [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 11:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[S] (S) ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 12:
 0   1   2   3   4   5   6
[S] [S] (.) ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 13:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]


Picosecond 14:
 0   1   2   3   4   5   6
[ ] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]


Picosecond 15:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... ... [ ] (.) [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]


Picosecond 16:
 0   1   2   3   4   5   6
[S] [S] ... ... [ ] ... ( )
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Because all smaller delays would get you caught,
the fewest number of picoseconds you would need to delay to get through safely is 10.

What is the fewest number of picoseconds
that you need to delay the packet to pass through the firewall without being caught?
"""

from itertools import count
from typing import NamedTuple

from parse import parse

type Firewall = list[Layer]


class Layer(NamedTuple):
    index: int
    depth: int


def get_delay(raw_firewall: list[str]) -> int:
    firewall = list(map(_parse_layer, raw_firewall))

    for delay in count(1):
        for layer in firewall:
            pos = _get_scanner_pos(delay + layer.index, layer.depth)
            if pos == 0:
                break
        else:
            break

    return delay


def _get_scanner_pos(tick: int, depth: int) -> int | None:
    if depth == 0:
        return None

    max_index = depth - 1
    turn_around = max_index * 2
    offset = tick % turn_around

    if offset > max_index:
        return turn_around - offset
    return offset


def _parse_layer(raw_layer: str) -> Layer:
    return Layer(*parse("{:d}: {:d}", raw_layer).fixed)


assert _parse_layer("0: 3") == Layer(0, 3)

assert _get_scanner_pos(0, 2) == 0
assert _get_scanner_pos(1, 2) == 1
assert _get_scanner_pos(2, 2) == 0
assert _get_scanner_pos(3, 2) == 1

assert _get_scanner_pos(0, 4) == 0
assert _get_scanner_pos(1, 4) == 1
assert _get_scanner_pos(2, 4) == 2
assert _get_scanner_pos(3, 4) == 3
assert _get_scanner_pos(4, 4) == 2
assert _get_scanner_pos(5, 4) == 1
assert _get_scanner_pos(6, 4) == 0
assert _get_scanner_pos(7, 4) == 1
assert _get_scanner_pos(8, 4) == 2
assert _get_scanner_pos(9, 4) == 3
assert _get_scanner_pos(10, 4) == 2

firewall = [
    "0: 3",
    "1: 2",
    "4: 4",
    "6: 4",
]
assert get_delay(firewall) == 10


with open("2017/13_packet_scanners/input.txt") as f:
    lines = [line.strip() for line in f]
    print(get_delay(lines))
