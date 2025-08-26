"""
The next year, just to show off,
Santa decides to take the route with the longest distance instead.

He can still start and end at any two (different) locations he wants,
and he still must visit each location exactly once.

For example, given the distances above,
the longest route would be 982 via (for example) Dublin -> London -> Belfast.

What is the distance of the longest route?
"""

from itertools import chain, pairwise, permutations
from re import match


def slowest_traversal(distances: dict[tuple[str, str], int]):
    locations = set(chain.from_iterable(distances))

    maximal_distance = 0
    maximal_route = None

    for route in permutations(locations):
        current_distance = 0
        for start, end in pairwise(route):
            distance = distances.get((start, end)) or distances.get((end, start))
            current_distance += distance

        if current_distance > maximal_distance:
            maximal_distance = current_distance
            maximal_route = route

    return maximal_route, maximal_distance


paths = {
    ("London", "Dublin"): 464,
    ("London", "Belfast"): 518,
    ("Dublin", "Belfast"): 141,
}
assert slowest_traversal(paths) == (("Dublin", "London", "Belfast"), 982)


with open("2015/09_all_in_a_single_night/input.txt") as f:
    paths = {}
    for line in f:
        start, end, distance = match(r"(\w+) to (\w+) = (\d+)", line).groups()
        paths[(start, end)] = int(distance)

    print(slowest_traversal(paths))
