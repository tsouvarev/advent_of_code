"""
In all the commotion, you realize that you forgot to seat yourself.
At this point, you're pretty apathetic toward the whole thing,
and your happiness wouldn't really go up or down regardless of who you sit next to.
You assume everyone else would be just as ambivalent about sitting next to you, too.

So, add yourself to the list,
and give all happiness relationships that involve you a score of 0.

What is the total change in happiness
for the optimal seating arrangement that actually includes yourself?
"""

from itertools import chain, permutations


def sit(rules: dict) -> tuple[list, int]:
    personas = _unique(rules)
    max_happiness = 0
    best_seatings = None

    for seatings in permutations(personas):
        # for seating around the table: seatings ABC means there is also CA seating
        full_seatings = [*seatings, seatings[0]]

        happiness = _count_happiness(rules, full_seatings)

        if happiness > max_happiness:
            max_happiness = happiness
            best_seatings = seatings

    return best_seatings, max_happiness


def _add_person(rules: dict, new_person: str) -> dict:
    personas = _unique(rules)

    for person in personas:
        rules[(person, new_person)] = 0
        rules[(new_person, person)] = 0

    return rules


def _count_happiness(rules: dict, seatings: list) -> int:
    if len(seatings) == 1:
        return 0

    a, b = seatings[:2]
    return rules[(a, b)] + rules[(b, a)] + _count_happiness(rules, seatings[1:])


def _unique(seq):
    return list(dict.fromkeys(chain.from_iterable(seq)))


rules = {
    ("Alice", "Bob"): 54,
    ("Alice", "Carol"): -79,
    ("Alice", "David"): -2,
    ("Bob", "Alice"): 83,
    ("Bob", "Carol"): -7,
    ("Bob", "David"): -63,
    ("Carol", "Alice"): -62,
    ("Carol", "Bob"): 60,
    ("Carol", "David"): 55,
    ("David", "Alice"): 46,
    ("David", "Bob"): -7,
    ("David", "Carol"): 41,
}
assert sit(rules) == (("Alice", "Bob", "Carol", "David"), 330)


with open("2015/13_knights_of_the_dinner_table/input.txt") as f:
    rules = {}
    for rule in f:
        tokens = rule.strip("\n.").split(" ")
        happiness = int(tokens[3]) * (-1 if tokens[2] == "lose" else 1)
        rules[(tokens[0], tokens[-1])] = happiness

    rules = _add_person(rules, "me")

    print(sit(rules))
