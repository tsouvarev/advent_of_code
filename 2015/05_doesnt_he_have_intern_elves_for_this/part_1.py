"""
Santa needs help figuring out which strings in his text file are naughty or nice.

A nice string is one with all of the following properties:
-   It contains at least three vowels (aeiou only),
    like aei, xazegov, or aeiouaeiouaeiou.
-   It contains at least one letter that appears twice in a row,
    like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
-   It does not contain the strings ab, cd, pq, or xy,
    even if they are part of one of the other requirements.

For example:
-   ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...),
    a double letter (...dd...), and none of the disallowed substrings.
-   aaa is nice because it has at least three vowels and a double letter,
    even though the letters used by different rules overlap.
-   jchzalrnumimnmhp is naughty because it has no double letter.
-   haegwjzuvuyypxyu is naughty because it contains the string xy.
-   dvszwmarrgswjxmb is naughty because it contains only one vowel.

How many strings are nice?
"""

import string
from collections import Counter
from itertools import pairwise


def is_nice(input_str: str) -> int:
    forbidden_strings = ["ab", "cd", "pq", "xy"]
    for forbidden in forbidden_strings:
        if forbidden in input_str:
            return False

    for double_candidate in string.ascii_letters:
        if double_candidate * 2 in input_str:
            break
    else:
        return False

    counted = Counter(input_str)
    return not sum(counted.get(vowel, 0) for vowel in "aeiou") < 3


FORBIDDEN_PAIRINGS = {("a", "b"), ("c", "d"), ("p", "q"), ("x", "y")}


def is_nice(input_str: str) -> int:
    # we check only first symbol of pair on being vowel,
    # so the last symbol of input should be checked too
    has_double, vowels_count = False, input_str[-1] in "aeiou"

    for a, b in pairwise(input_str):
        if (a, b) in FORBIDDEN_PAIRINGS:
            return False

        if a == b:
            has_double = True

        if a in "aeiou":
            vowels_count += 1

    return vowels_count >= 3 and has_double


assert is_nice("ugknbfddgicrmopn") is True
assert is_nice("aaa") is True
assert is_nice("jchzalrnumimnmhp") is False
assert is_nice("haegwjzuvuyypxyu") is False
assert is_nice("dvszwmarrgswjxmb") is False


with open("2015/05_doesnt_he_have_intern_elves_for_this/input.txt") as f:
    print(len([line for line in f if is_nice(line)]))
