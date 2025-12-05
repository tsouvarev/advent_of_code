"""
The Elves have good news and bad news.

The good news is that they've discovered project management!
This has given them the tools they need to prevent their usual Christmas emergency.
For example, they now know that the North Pole decorations need to be finished soon
so that other critical tasks can start on time.

The bad news is that they've realized they have a different emergency:
according to their resource planning, none of them have any time left
to decorate the North Pole!

To save Christmas, the Elves need you to finish decorating the North Pole
by December 12th.

Collect stars by solving puzzles. Two puzzles will be made available on each day;
the second puzzle is unlocked when you complete the first.
Each puzzle grants one star. Good luck!

You arrive at the secret entrance to the North Pole base ready to start decorating.
Unfortunately, the password seems to have been changed, so you can't get in.
A document taped to the wall helpfully explains:

"Due to new security protocols, the password is locked in the safe below.
Please see the attached document for the new combination."

The safe has a dial with only an arrow on it;
around the dial are the numbers 0 through 99 in order.
As you turn the dial, it makes a small click noise as it reaches each number.

The attached document (your puzzle input) contains a sequence of rotations,
one per line, which tell you how to open the safe.
A rotation starts with an L or R which indicates
whether the rotation should be to the left (toward lower numbers)
or to the right (toward higher numbers).
Then, the rotation has a distance value which indicates
how many clicks the dial should be rotated in that direction.

So, if the dial were pointing at 11,
a rotation of R8 would cause the dial to point at 19.
After that, a rotation of L19 would cause it to point at 0.

Because the dial is a circle,
turning the dial left from 0 one click makes it point at 99.
Similarly, turning the dial right from 99 one click makes it point at 0.

So, if the dial were pointing at 5, a rotation of L10 would cause it to point at 95.
After that, a rotation of R5 could cause it to point at 0.

The dial starts by pointing at 50.

You could follow the instructions,
but your recent required official North Pole secret entrance security training seminar
taught you that the safe is actually a decoy.
The actual password is the number of times the dial is left pointing at 0
after any rotation in the sequence.

For example, suppose the attached document contained the following rotations:

L68
L30
R48
L5
R60
L55
L1
L99
R14
L82

Following these rotations would cause the dial to move as follows:

- The dial starts by pointing at 50.
- The dial is rotated L68 to point at 82.
- The dial is rotated L30 to point at 52.
- The dial is rotated R48 to point at 0.
- The dial is rotated L5 to point at 95.
- The dial is rotated R60 to point at 55.
- The dial is rotated L55 to point at 0.
- The dial is rotated L1 to point at 99.
- The dial is rotated L99 to point at 0.
- The dial is rotated R14 to point at 14.
- The dial is rotated L82 to point at 32.

Because the dial points at 0 a total of three times during this process,
the password in this example is 3.

Analyze the rotations in your attached document.
What's the actual password to open the door?
"""

from enum import StrEnum, auto
from typing import NamedTuple


class Rotation(NamedTuple):
    direction: Direction
    n: int


class Direction(StrEnum):
    LEFT = auto()
    RIGHT = auto()


def get_code(raw_rotations: list[str], *, start: int = 50) -> int:
    pos, max_rotation = start, 100
    code = 0

    for raw_rotation in raw_rotations:
        rotation = _parse_rotation(raw_rotation)
        pos = _rotate(pos, rotation, max_rotation)

        if pos == 0:
            code += 1

    return code


def _rotate(current: int, rotation: Rotation, max_rotation: int) -> int:
    if rotation.direction == Direction.RIGHT:
        return (current + rotation.n) % max_rotation

    return (max_rotation + current - rotation.n) % max_rotation


def _parse_rotation(raw_rotation: str) -> Rotation:
    raw_direction, *raw_n = raw_rotation

    match raw_direction:
        case "R":
            direction = Direction.RIGHT
        case "L":
            direction = Direction.LEFT
        case _:
            raise ValueError(raw_rotation)

    return Rotation(direction, int("".join(raw_n)))


assert _parse_rotation("R48") == Rotation(Direction.RIGHT, 48)
assert _parse_rotation("L5") == Rotation(Direction.LEFT, 5)

assert _rotate(0, Rotation(Direction.LEFT, 1), 10) == 9
assert _rotate(0, Rotation(Direction.LEFT, 11), 10) == 9
assert _rotate(1, Rotation(Direction.LEFT, 1), 10) == 0
assert _rotate(8, Rotation(Direction.LEFT, 1), 10) == 7
assert _rotate(8, Rotation(Direction.LEFT, 11), 10) == 7
assert _rotate(8, Rotation(Direction.LEFT, 9), 10) == 9

assert _rotate(0, Rotation(Direction.RIGHT, 1), 10) == 1
assert _rotate(0, Rotation(Direction.RIGHT, 11), 10) == 1
assert _rotate(9, Rotation(Direction.RIGHT, 1), 10) == 0
assert _rotate(8, Rotation(Direction.RIGHT, 1), 10) == 9

rotations = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]
assert get_code(rotations, start=50) == 3


with open("2025/01_secret_entrance/input.txt") as f:
    rotations = [line.strip() for line in f]
    print(get_code(rotations, start=50))
