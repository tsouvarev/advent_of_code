"""
Something is jamming your communications with Santa.
Fortunately, your signal is only partially jammed,
and protocol in situations like this is
to switch to a simple repetition code to get the message through.

In this model, the same message is sent repeatedly.
You've recorded the repeating message signal (your puzzle input),
but the data seems quite corrupted - almost too badly to recover. Almost.

All you need to do is figure out which character is most frequent for each position.
For example, suppose you had recorded the following messages:

eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar

The most common character in the first column is e; in the second, a and so on.
Combining these characters returns the error-corrected message, easter.

Given the recording in your puzzle input,
what is the error-corrected version of the message being sent?
"""

from collections import Counter


def unjam(signals: list[str]) -> str:
    common_chars = map(_get_most_common_char, zip(*signals))
    return "".join(common_chars)


def _get_most_common_char(chars: list[str]) -> str:
    return Counter(chars).most_common(1)[0][0]


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
assert unjam(signals) == "easter"


with open("2016/06_signals_and_noise/input.txt") as f:
    print(unjam(f.read().splitlines()))
