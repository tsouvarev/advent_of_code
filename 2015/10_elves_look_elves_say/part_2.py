"""
Now, starting again with the digits in your puzzle input, apply this process 50 times.
What is the length of the new result?
"""

from itertools import chain, groupby, starmap


def look_and_say(seq: str) -> str:
    return "".join(chain.from_iterable(starmap(_say, groupby(seq))))


def _say(grouper, group):
    group_len = str(len(list(group)))
    return group_len, grouper


assert look_and_say("1") == "11"
assert look_and_say("11") == "21"
assert look_and_say("21") == "1211"
assert look_and_say("1211") == "111221"
assert look_and_say("111221") == "312211"


res = "1113122113"
for _ in range(50):
    res = look_and_say(res)

print(len(res))
