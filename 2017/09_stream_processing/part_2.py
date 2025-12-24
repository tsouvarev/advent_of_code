"""
Now, you're ready to remove the garbage.

To prove you've removed it, you need to count all of the characters within the garbage.
The leading and trailing < and > don't count,
nor do any canceled characters
or the ! doing the canceling.

- <>, 0 characters.
- <random characters>, 17 characters.
- <<<<>, 3 characters.
- <{!>}>, 2 characters.
- <!!>, 0 characters.
- <!!!>>, 0 characters.
- <{o"i!a,<{i<a>, 10 characters.

How many non-canceled characters are within the garbage in your puzzle input?
"""

from collections.abc import Iterator


def count_garbage(stream: str) -> int:
    garbage = _keep_garbage(stream)
    return sum(map(len, garbage))


def _keep_garbage(stream: str) -> Iterator[str]:
    ignore_next, inside_garbage = False, False

    for c in stream:
        if ignore_next:
            ignore_next = False
            continue

        match c:
            case "!":
                ignore_next = True
            case "<" if not inside_garbage:
                inside_garbage = True
            case ">":
                inside_garbage = False
            case _:
                if inside_garbage:
                    yield c


assert count_garbage("<>") == 0
assert count_garbage("<random characters>") == 17
assert count_garbage("<<<<>") == 3
assert count_garbage("<{!>}>") == 2
assert count_garbage("<!!>") == 0
assert count_garbage("<!!!>0") == 1
assert count_garbage('<{o"i!a,<{i<a>') == 10


with open("2017/09_stream_processing/input.txt") as f:
    print(count_garbage(f.read()))
