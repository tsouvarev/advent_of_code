"""
Of course, that would be the message -
if you hadn't agreed to use a modified repetition code instead.

In this modified code, the sender instead transmits what looks like random data,
but for each character, the character they actually want to send
is slightly less likely than the others.
Even after signal-jamming noise, you can look at the letter distributions
in each column and choose the least common letter to reconstruct the original message.

In the above example, the least common character in the first column is a;
in the second, d, and so on.
Repeating this process for the remaining characters produces the message, advent.

Given the recording in your puzzle input and this new decoding methodology,
what is the original message that Santa is trying to send?
"""

from collections import Counter


def unjam(signals: list[str]) -> str:
    uncommon_chars = map(_get_least_common_char, zip(*signals))
    return "".join(uncommon_chars)


def _get_least_common_char(chars: list[str]) -> str:
    return Counter(chars).most_common()[-1][0]


assert unjam(["eedadn"]) == "eedadn"
signals = [
    "eedadn",
    "drvtee",
    "eandsr",
    "raavrd",
    "atevrs",
    "tsrnev",
    "sdttsa",
    "rasrtv",
    "nssdts",
    "ntnada",
    "svetve",
    "tesnvt",
    "vntsnd",
    "vrdear",
    "dvrsen",
    "enarar",
]
assert unjam(signals) == "advent"


with open("2016/06_signals_and_noise/input.txt") as f:
    print(unjam(f.read().splitlines()))
