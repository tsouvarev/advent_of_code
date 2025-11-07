"""
The computer system you're breaking into
uses a weird scrambling function to store its passwords.
It shouldn't be much trouble to create your own scrambled password
so you can add it to the system; you just have to implement the scrambler.

The scrambling function is a series of operations
(the exact list is provided in your puzzle input).
Starting with the password to be scrambled,
apply each operation in succession to the string.
The individual operations behave as follows:

-   swap position X with position Y means that
    the letters at indexes X and Y (counting from 0) should be swapped.
-   swap letter X with letter Y means that
    the letters X and Y should be swapped
    (regardless of where they appear in the string).
-   rotate left/right X steps means that
    the whole string should be rotated;
    for example, one right rotation would turn abcd into dabc.
-   rotate based on position of letter X means that
    the whole string should be rotated to the right
    based on the index of letter X (counting from 0)
    as determined before this instruction does any rotations.
    Once the index is determined, rotate the string to the right one time,
    plus a number of times equal to that index,
    plus one additional time if the index was at least 4.
-   reverse positions X through Y means that
    the span of letters at indexes X through Y
    (including the letters at X and Y) should be reversed in order.
-   move position X to position Y means that
    the letter which is at index X should be removed from the string,
    then inserted such that it ends up at index Y.

For example, suppose you start with abcde and perform the following operations:

-   swap position 4 with position 0
    swaps the first and last letters, producing the input for the next step, ebcda.
-   swap letter d with letter b swaps the positions of d and b: edcba.
-   reverse positions 0 through 4
    causes the entire string to be reversed, producing abcde.
-   rotate left 1 step
    shifts all letters left one position,
    causing the first letter to wrap to the end of the string: bcdea.
-   move position 1 to position 4
    removes the letter at position 1 (c),
    then inserts it at position 4 (the end of the string): bdeac.
-   move position 3 to position 0
    removes the letter at position 3 (a),
    then inserts it at position 0 (the front of the string): abdec.
-   rotate based on position of letter b
    finds the index of letter b (1),
    then rotates the string right once
    plus a number of times equal to that index (2): ecabd.
-   rotate based on position of letter d
    finds the index of letter d (4),
    then rotates the string right once,
    plus a number of times equal to that index,
    plus an additional time because the index was at least 4,
    for a total of 6 right rotations: decab.

After these steps, the resulting scrambled password is decab.

Now, you just need to generate a new scrambled password and you can access the system.
Given the list of scrambling operations in your puzzle input,
what is the result of scrambling abcdefgh?
"""

from collections.abc import Callable, Iterator
from enum import StrEnum, auto
from typing import NamedTuple

from parse import parse


class Op(StrEnum):
    SWAP_POSITIONS = auto()  # swap position 4 with position 1
    SWAP_LETTERS = auto()  # swap letter d with letter c
    ROTATE_LEFT = auto()  # rotate left 0 steps
    ROTATE_RIGHT = auto()  # rotate right 0 steps
    ROTATE_POSITION = auto()  # rotate based on position of letter a
    REVERSE = auto()  # reverse positions 1 through 6
    MOVE = auto()  # move position 5 to position 7


class Instruction(NamedTuple):
    op: Op
    args: list
    handler: Callable


def scramble(password: list[str], instructions: list[str]) -> str:
    for raw_instruction in instructions:
        i = _parse_instruction(raw_instruction)
        password = list(i.handler(password, *i.args))
    return "".join(password)


def _swap_positions(s: list[str], pos_from: int, pos_to: int) -> Iterator[str]:
    letter_from, letter_to = s[pos_from], s[pos_to]

    for i, c in enumerate(s):
        if i == pos_from:
            yield letter_to
        elif i == pos_to:
            yield letter_from
        else:
            yield c


def _swap_letters(s: list[str], letter_a: str, letter_b: str) -> Iterator[str]:
    for c in s:
        if c == letter_a:
            yield letter_b
        elif c == letter_b:
            yield letter_a
        else:
            yield c


def _rotate_left(s: list[str], steps: int) -> Iterator[str]:
    shift = steps % len(s)
    yield from s[shift:]
    yield from s[:shift]


def _rotate_right(s: list[str], steps: int) -> Iterator[str]:
    shift = steps % len(s)
    yield from s[-shift:]
    yield from s[:-shift]


def _rotate_position(s: list[str], letter: str) -> Iterator[str]:
    letter_pos = s.index(letter)
    shift = 1 + letter_pos + (1 if letter_pos > 3 else 0)
    yield from _rotate_right(s, shift)


def _reverse_positions(s: list[str], pos_start: int, pos_end: int) -> Iterator[str]:
    yield from s[:pos_start]
    yield from reversed(s[pos_start : pos_end + 1])
    yield from s[pos_end + 1 :]


def _move_positions(s: list[str], pos_a: int, pos_b: int) -> Iterator[str]:
    c = s.pop(pos_a)
    s.insert(pos_b, c)
    yield from s


def _parse_instruction(raw_instruction: str) -> Instruction:
    specs = [
        ("swap position {:d} with position {:d}", Op.SWAP_POSITIONS, _swap_positions),
        ("swap letter {} with letter {}", Op.SWAP_LETTERS, _swap_letters),
        ("rotate left {:d} step", Op.ROTATE_LEFT, _rotate_left),
        ("rotate left {:d} steps", Op.ROTATE_LEFT, _rotate_left),
        ("rotate right {:d} step", Op.ROTATE_RIGHT, _rotate_right),
        ("rotate right {:d} steps", Op.ROTATE_RIGHT, _rotate_right),
        ("rotate based on position of letter {}", Op.ROTATE_POSITION, _rotate_position),
        ("reverse positions {:d} through {:d}", Op.REVERSE, _reverse_positions),
        ("move position {:d} to position {:d}", Op.MOVE, _move_positions),
    ]
    for spec, op, handler in specs:
        if parsed := parse(spec, raw_instruction):
            return Instruction(op, parsed.fixed, handler)

    raise ValueError(raw_instruction)


assert "".join(_swap_positions(list("abc"), 0, 1)) == "bac"
assert "".join(_swap_positions(list("abc"), 1, 0)) == "bac"

assert "".join(_swap_letters(list("abac"), "a", "b")) == "babc"
assert "".join(_swap_letters(list("abac"), "d", "b")) == "adac"

assert "".join(_rotate_left(list("abc"), 2)) == "cab"
assert "".join(_rotate_left(list("abc"), 5)) == "cab"

assert "".join(_rotate_right(list("abc"), 2)) == "bca"
assert "".join(_rotate_right(list("abc"), 5)) == "bca"

assert "".join(_rotate_position(list("abc"), "b")) == "bca"
assert "".join(_rotate_position(list("abcdef"), "e")) == "abcdef"
assert "".join(_rotate_position(list("ecabd"), "d")) == "decab"

assert "".join(_reverse_positions(list("abcdef"), 1, 3)) == "adcbef"

assert "".join(_move_positions(list("abcdef"), 1, 3)) == "acdbef"

instructions = [
    "swap position 4 with position 0",
    "swap letter d with letter b",
    "reverse positions 0 through 4",
    "rotate left 1 step",
    "move position 1 to position 4",
    "move position 3 to position 0",
    "rotate based on position of letter b",
    "rotate based on position of letter d",
]
assert scramble(list("abcde"), instructions) == "decab"

with open("2016/21_scrambled_letters_and_hash/input.txt") as f:
    print(scramble(list("abcdefgh"), [l.strip() for l in f]))
