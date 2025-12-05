"""
You're sure that's the right password, but the door won't open.
You knock, but nobody answers. You build a snowman while you think.

As you're rolling the snowballs for your snowman,
you find another security document that must have fallen into the snow:

"Due to newer security protocols,
please use password method 0x434C49434B until further notice."

You remember from the training seminar that "method 0x434C49434B" means
you're actually supposed to count the number of times
any click causes the dial to point at 0,
regardless of whether it happens during a rotation or at the end of one.

Following the same rotations as in the above example,
the dial points at zero a few extra times during its rotations:

- The dial starts by pointing at 50.
- The dial is rotated L68 to point at 82; during this rotation, it points at 0 once.
- The dial is rotated L30 to point at 52.
- The dial is rotated R48 to point at 0.
- The dial is rotated L5 to point at 95.
- The dial is rotated R60 to point at 55; during this rotation, it points at 0 once.
- The dial is rotated L55 to point at 0.
- The dial is rotated L1 to point at 99.
- The dial is rotated L99 to point at 0.
- The dial is rotated R14 to point at 14.
- The dial is rotated L82 to point at 32; during this rotation, it points at 0 once.

In this example, the dial points at 0 three times at the end of a rotation,
plus three more times during a rotation.
So, in this example, the new password would be 6.

Be careful: if the dial were pointing at 50,
a single rotation like R1000 would cause the dial to point at 0
ten times before returning back to 50!

Using password method 0x434C49434B, what is the password to open the door?
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
        pos, zeros = _rotate(pos, rotation, max_rotation)
        code += zeros

    return code


def _rotate(pos: int, rotation: Rotation, max_rotation: int) -> tuple[int, int]:
    if rotation.direction == Direction.RIGHT:
        new_pos = (pos + rotation.n) % max_rotation
        num_zeros = (pos + rotation.n) // max_rotation
        return new_pos, num_zeros

    new_pos = (max_rotation + pos - rotation.n) % max_rotation

    if pos > rotation.n:
        num_zeros = 0
    else:
        num_zeros = (rotation.n - pos) // max_rotation + (pos != 0)

    return new_pos, num_zeros


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

assert _rotate(0, Rotation(Direction.LEFT, 1), 10) == (9, 0)
assert _rotate(0, Rotation(Direction.LEFT, 11), 10) == (9, 1)
assert _rotate(1, Rotation(Direction.LEFT, 1), 10) == (0, 1)
assert _rotate(8, Rotation(Direction.LEFT, 1), 10) == (7, 0)
assert _rotate(8, Rotation(Direction.LEFT, 11), 10) == (7, 1)
assert _rotate(8, Rotation(Direction.LEFT, 21), 10) == (7, 2)
assert _rotate(8, Rotation(Direction.LEFT, 9), 10) == (9, 1)

assert _rotate(0, Rotation(Direction.RIGHT, 1), 10) == (1, 0)
assert _rotate(0, Rotation(Direction.RIGHT, 11), 10) == (1, 1)
assert _rotate(0, Rotation(Direction.RIGHT, 21), 10) == (1, 2)
assert _rotate(9, Rotation(Direction.RIGHT, 1), 10) == (0, 1)
assert _rotate(8, Rotation(Direction.RIGHT, 1), 10) == (9, 0)

rotations = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]
assert get_code(rotations, start=50) == 6


with open("2025/01_secret_entrance/input.txt") as f:
    rotations = [line.strip() for line in f]
    print(get_code(rotations, start=50))
