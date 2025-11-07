"""
You scrambled the password correctly,
but you discover that you can't actually modify the password file on the system.
You'll need to un-scramble one of the existing passwords
by reversing the scrambling process.

What is the un-scrambled version of the scrambled password fbgdceah?
"""

from collections.abc import Callable, Iterator
from typing import NamedTuple

from parse import parse


class Instruction(NamedTuple):
    handler: Callable
    args: list


def unscramble(password: list[str], instructions: list[str]) -> str:
    for raw_instruction in reversed(instructions):
        i = _parse_instruction(raw_instruction)
        password = list(i.handler(password, *i.args))
    return "".join(password)


def _unswap_positions(s: list[str], pos_from: int, pos_to: int) -> Iterator[str]:
    letter_from, letter_to = s[pos_from], s[pos_to]

    for i, c in enumerate(s):
        if i == pos_from:
            yield letter_to
        elif i == pos_to:
            yield letter_from
        else:
            yield c


def _unswap_letters(s: list[str], letter_a: str, letter_b: str) -> Iterator[str]:
    for c in s:
        if c == letter_a:
            yield letter_b
        elif c == letter_b:
            yield letter_a
        else:
            yield c


def _unrotate_left(s: list[str], steps: int) -> Iterator[str]:
    shift = steps % len(s)
    yield from s[-shift:]
    yield from s[:-shift]


def _unrotate_right(s: list[str], steps: int) -> Iterator[str]:
    shift = steps % len(s)
    yield from s[shift:]
    yield from s[:shift]


def _unrotate_position(s: list[str], letter: str) -> list[str]:
    for maybe_shift in range(len(s)):
        candidate = list(_unrotate_right(s, maybe_shift))
        if list(_rotate_position(candidate, letter)) == s:
            return candidate

    raise ValueError


def _rotate_position(s: list[str], letter: str) -> Iterator[str]:
    letter_pos = s.index(letter)
    shift = 1 + letter_pos + (1 if letter_pos > 3 else 0)
    yield from _unrotate_left(s, shift)


def _unreverse_positions(s: list[str], pos_start: int, pos_end: int) -> Iterator[str]:
    yield from s[:pos_start]
    yield from reversed(s[pos_start : pos_end + 1])
    yield from s[pos_end + 1 :]


def _unmove_positions(s: list[str], pos_a: int, pos_b: int) -> Iterator[str]:
    c = s.pop(pos_b)
    s.insert(pos_a, c)
    yield from s


def _parse_instruction(raw_instruction: str) -> Instruction:
    specs = [
        ("swap position {:d} with position {:d}", _unswap_positions),
        ("swap letter {} with letter {}", _unswap_letters),
        ("rotate left {:d} step", _unrotate_left),
        ("rotate left {:d} steps", _unrotate_left),
        ("rotate right {:d} step", _unrotate_right),
        ("rotate right {:d} steps", _unrotate_right),
        ("rotate based on position of letter {}", _unrotate_position),
        ("reverse positions {:d} through {:d}", _unreverse_positions),
        ("move position {:d} to position {:d}", _unmove_positions),
    ]
    for spec, handler in specs:
        if parsed := parse(spec, raw_instruction):
            return Instruction(handler, parsed.fixed)

    raise ValueError(raw_instruction)


assert "".join(_unswap_positions(list("bac"), 0, 1)) == "abc"

assert "".join(_unswap_letters(list("abac"), "a", "b")) == "babc"
assert "".join(_unswap_letters(list("abac"), "d", "b")) == "adac"

assert "".join(_unrotate_left(list("abc"), 2)) == "bca"
assert "".join(_unrotate_left(list("abc"), 5)) == "bca"

assert "".join(_unrotate_right(list("abc"), 2)) == "cab"
assert "".join(_unrotate_right(list("abc"), 5)) == "cab"

assert "".join(_unrotate_position(list("abc"), "b")) == "bca"
assert "".join(_unrotate_position(list("abcdef"), "e")) == "abcdef"

assert "".join(_unreverse_positions(list("abcdef"), 1, 3)) == "adcbef"

assert "".join(_unmove_positions(list("abcdef"), 1, 3)) == "adbcef"

with open("2016/21_scrambled_letters_and_hash/input.txt") as f:
    print(unscramble(list("fbgdceah"), [l.strip() for l in f]))
