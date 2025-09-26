"""
In years past, the holiday feast with your family hasn't gone so well.
Not everyone gets along! This year, you resolve, will be different.
You're going to find the optimal seating arrangement
and avoid all those awkward conversations.

You start by writing up a list of everyone invited
and the amount their happiness would increase or decrease
if they were to find themselves sitting next to each other person.
You have a circular table that will be just big enough to fit everyone comfortably,
and so each person will have exactly two neighbors.

For example, suppose you have only four attendees planned,
and you calculate their potential happiness as follows:

Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.

Then, if you seat Alice next to David,
Alice would lose 2 happiness units (because David talks so much),
but David would gain 46 happiness units (because Alice is such a good listener),
for a total change of 44.

If you continue around the table,
you could then seat Bob next to Alice (Bob gains 83, Alice gains 54).
Finally, seat Carol, who sits next to Bob (Carol gains 60, Bob loses 7)
and David (Carol gains 55, David gains 41). The arrangement looks like this:

     +41 +46
+55   David    -2
Carol       Alice
+60    Bob    +54
     -7  +83

After trying every other seating arrangement in this hypothetical scenario,
you find that this one is the most optimal, with a total change in happiness of 330.

What is the total change in happiness
for the optimal seating arrangement of the actual guest list?
"""

from itertools import chain, pairwise, permutations


def sit(rules: dict) -> list:
    personas = _unique(rules)
    max_happiness = 0
    best_seatings = None

    for seatings in permutations(personas):
        happiness = _count_happiness(rules, seatings)

        if happiness > max_happiness:
            max_happiness = happiness
            best_seatings = seatings

    return best_seatings, max_happiness


def _count_happiness(rules: dict, seatings: list) -> int:
    # for seating around the table: seatings ABC means there is also CA seating
    full_seatings = [*seatings, seatings[0]]
    return sum(rules[(a, b)] + rules[(b, a)] for a, b in pairwise(full_seatings))


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
assert _count_happiness(rules, ("Alice", "Bob", "Carol", "David")) == 330


with open("2015/13_knights_of_the_dinner_table/input.txt") as f:
    rules = {}
    for rule in f:
        tokens = rule.strip("\n.").split(" ")
        happiness = int(tokens[3]) * (-1 if tokens[2] == "lose" else 1)
        rules[(tokens[0], tokens[-1])] = happiness

    print(sit(rules))
