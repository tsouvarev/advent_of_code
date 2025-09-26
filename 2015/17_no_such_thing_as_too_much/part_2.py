"""
While playing with all the containers in the kitchen, another load of eggnog arrives!
The shipping and receiving department is requesting as many containers as you can spare.

Find the minimum number of containers that can exactly fit all 150 liters of eggnog.
How many different ways can you fill that number of containers
and still hold exactly 150 litres?

In the example above, the minimum number of containers was two.
There were three ways to use that many containers, and so the answer there would be 3.
"""

from collections import Counter
from itertools import combinations


def len_containers(containers: list[int], volume: int) -> dict:
    res = []
    for l in range(2, len(containers) + 1):
        for combination in combinations(containers, l):
            if sum(combination) == volume:
                res.append(combination)  # noqa: PERF401

    return Counter(map(len, res))


assert len_containers([20, 15, 10, 5, 5], 25) == {2: 3, 3: 1}

with open("2015/17_no_such_thing_as_too_much/input.txt") as f:
    containers = list(map(int, f.readlines()))
    print(len_containers(containers, 150))
