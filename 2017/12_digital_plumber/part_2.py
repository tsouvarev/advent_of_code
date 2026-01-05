"""
There are more programs than just the ones in the group containing program ID 0.
The rest of them have no way of reaching that group,
and still might have no way of reaching each other.

A group is a collection of programs
that can all communicate via pipes either directly or indirectly.
The programs you identified just a moment ago are all part of the same group.
Now, they would like you to determine the total number of groups.

In the example above, there were 2 groups:
one consisting of programs 0,2,3,4,5,6, and the other consisting solely of program 1.

How many groups are there in total?
"""

from collections import deque

type Pipe = tuple[int, list[int]]


def connect_pipes(raw_pipes: list[str]) -> int:
    pipes = dict(map(_parse_pipe, raw_pipes))
    groups = []

    while pipes:
        start = next(iter(pipes))
        queue = deque([start])
        group = set()

        while queue:
            node = queue.pop()
            group.add(node)

            for neighbor in pipes.pop(node, []):
                if neighbor not in group:
                    queue.append(neighbor)

        groups.append(group)

    return len(groups)


def _parse_pipe(raw_pipe: str) -> Pipe:
    from_, to_ = raw_pipe.split(" <-> ")
    return int(from_), [int(t) for t in to_.split(", ")]


assert _parse_pipe("0 <-> 2") == (0, [2])

raw_pipes = [
    "0 <-> 2",
    "1 <-> 1",
    "2 <-> 0, 3, 4",
    "3 <-> 2, 4",
    "4 <-> 2, 3, 6",
    "5 <-> 6",
    "6 <-> 4, 5",
]
assert connect_pipes(raw_pipes) == 2


with open("2017/12_digital_plumber/input.txt") as f:
    lines = [line.strip() for line in f]
    print(connect_pipes(lines))
