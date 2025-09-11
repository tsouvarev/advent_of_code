"""
Santa's previous password expired, and he needs help choosing a new one.

To help him remember his new password after the old one expires,
Santa has devised a method of coming up with a password based on the previous one.
Corporate policy dictates that passwords must be
exactly eight lowercase letters (for security reasons), so he finds his new password
by incrementing his old password string repeatedly until it is valid.

Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on.
Increase the rightmost letter one step;
if it was z, it wraps around to a,
and repeat with the next letter to the left until one doesn't wrap around.

Unfortunately for Santa, a new Security-Elf recently started,
and he has imposed some additional password requirements:

-   Passwords must include one increasing straight of at least three letters,
    like abc, bcd, cde, and so on, up to xyz.
    They cannot skip letters; abd doesn't count.
-   Passwords may not contain the letters i, o, or l,
    as these letters can be mistaken for other characters and are therefore confusing.
-   Passwords must contain at least two different,
    non-overlapping pairs of letters, like aa, bb, or zz.

For example:

-   hijklmmn meets the first requirement (because it contains the straight hij)
    but fails the second requirement requirement (because it contains i and l).
-   abbceffg meets the third requirement (because it repeats bb and ff)
    but fails the first requirement.
-   abbcegjk fails the third requirement, because it only has one double letter (bb).
-   The next password after abcdefgh is abcdffaa.
-   The next password after ghijklmn is ghjaabcc,
    because you eventually skip all the passwords that start with ghi...,
    since i is not allowed.

Given Santa's current password (your puzzle input), what should his next password be?
"""

import string
from itertools import pairwise, tee

FORBIDDEN_LETTERS = {"i", "o", "l"}


def get_next_password(password: str) -> str:
    while True:
        password = _skip_forbidden_tail(password)
        password = _incr_password(password)

        if _has_increasing_straight_of_3(password) and _has_pairs(password):
            return password


def _skip_forbidden_tail(password: str) -> str:
    new_password = []

    for i, c in enumerate(password):
        if c not in FORBIDDEN_LETTERS:
            new_password.append(c)
        else:
            tail_len = len(password) - i - 1
            new_password.append(_incr_char(c))
            new_password.extend("a" * tail_len)
            break

    return "".join(new_password)


def _incr_password(password: str) -> str:
    new_password = []
    reversed_password = reversed(password)

    for c in reversed_password:
        if c == "z":
            new_password.append("a")
        else:
            new_password.append(_incr_char(c))
            new_password.extend(reversed_password)
            break

    return "".join(reversed(new_password))


def _incr_char(c: str) -> str:
    return chr(ord(c) + 1)


def _has_increasing_straight_of_3(password: str) -> bool:
    return any(straight in password for straight in STRAIGHTS_OF_3)


def _has_pairs(password: str) -> bool:
    pairs = 0
    skip_next = False

    for c, c_next in pairwise(password):
        if skip_next:
            skip_next = False
            continue

        if c == c_next:
            pairs += 1
            skip_next = True

    return pairs == 2


def _triplewise(iterable):
    t1, t2, t3 = tee(iterable, 3)
    next(t3, None)
    next(t3, None)
    next(t2, None)
    return zip(t1, t2, t3)


STRAIGHTS_OF_3 = set(map("".join, _triplewise(string.ascii_lowercase)))


assert _incr_char("a") == "b"

assert _incr_password("a") == "b"
assert _incr_password("z") == "a"
assert _incr_password("zz") == "aa"
assert _incr_password("xx") == "xy"
assert _incr_password("abcdxz") == "abcdya"

assert _skip_forbidden_tail("aai") == "aaj"
assert _skip_forbidden_tail("aia") == "aja"

assert _has_increasing_straight_of_3("abc") is True
assert _has_increasing_straight_of_3("xyz") is True
assert _has_increasing_straight_of_3("abd") is False
assert _has_increasing_straight_of_3("yz") is False

assert _has_pairs("aabb") is True
assert _has_pairs("asdaaasdbbasd") is True
assert _has_pairs("aaa") is False
assert _has_pairs("aaba") is False


assert get_next_password("abcdefgh") == "abcdffaa"
assert get_next_password("ghijklmn") == "ghjaabcc"

print(get_next_password("hepxcrrq"))
print(get_next_password("hepxxyzz"))
