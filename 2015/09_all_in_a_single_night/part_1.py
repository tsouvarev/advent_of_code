"""
Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit;
his elves have provided him the distances between every pair of locations.
He can start and end at any two (different) locations he wants,
but he must visit each location exactly once.
What is the shortest distance he can travel to achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141

The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982

The shortest of these is London -> Dublin -> Belfast = 605,
and so the answer is 605 in this example.

What is the distance of the shortest route?
"""

from itertools import chain, pairwise, permutations
from math import inf
from re import match


def fastest_traversal(distances: dict[tuple[str, str], int]):
    locations = set(chain.from_iterable(distances))

    minimal_distance = inf
    minimal_route = None

    for route in permutations(locations):
        current_distance = 0
        for start, end in pairwise(route):
            distance = distances.get((start, end)) or distances.get((end, start))
            current_distance += distance

        if current_distance < minimal_distance:
            minimal_distance = current_distance
            minimal_route = route

    return minimal_route, minimal_distance


paths = {
    ("London", "Dublin"): 464,
    ("London", "Belfast"): 518,
    ("Dublin", "Belfast"): 141,
}
assert fastest_traversal(paths) == (("London", "Dublin", "Belfast"), 605)


with open("2015/09_all_in_a_single_night/input.txt") as f:
    paths = {}
    for line in f:
        start, end, distance = match(r"(\w+) to (\w+) = (\d+)", line).groups()
        paths[(start, end)] = int(distance)

    print(fastest_traversal(paths))
