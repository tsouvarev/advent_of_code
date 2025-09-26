"""
The elves bought too much eggnog again - 150 liters this time.
To fit it all into your refrigerator, you'll need to move it into smaller containers.
You take an inventory of the capacities of the available containers.

For example, suppose you have containers of size 20, 15, 10, 5, and 5 liters.
If you need to store 25 liters, there are four ways to do it:

- 15 and 10
- 20 and 5 (the first 5)
- 20 and 5 (the second 5)
- 15, 5, and 5

Filling all containers entirely,
how many different combinations of containers can exactly fit all 150 liters of eggnog?
"""

from itertools import combinations


def fill_containers(containers: list[int], volume: int) -> list[tuple[int]]:
    res = []

    for l in range(2, len(containers) + 1):
        for combination in combinations(containers, l):
            if sum(combination) == volume:
                res.append(combination)  # noqa: PERF401

    return res


assert fill_containers([20, 15, 10, 5, 5], 25) == [
    (20, 5),
    (20, 5),
    (15, 10),
    (15, 5, 5),
]

with open("2015/17_no_such_thing_as_too_much/input.txt") as f:
    containers = list(map(int, f.readlines()))
    print(len(fill_containers(containers, 150)))
