"""
You finally arrive at the bathroom
(it's a several minute walk from the lobby
so visitors can behold the many fancy conference rooms and water coolers on this floor)
and go to punch in the code.
Much to your bladder's dismay, the keypad is not at all like you imagined it.
Instead, you are confronted with the result of hundreds of man-hours
of bathroom-keypad-design meetings:

    1
  2 3 4
5 6 7 8 9
  A B C
    D

You still start at "5" and stop when you're at an edge,
but given the same instructions as above, the outcome is very different:

-   You start at "5" and don't move at all (up and left are both edges), ending at 5.
-   Continuing from "5", you move right twice and down three times
    (through "6", "7", "B", "D", "D"), ending at D.
-   Then, from "D", you move five more times
    (through "D", "B", "C", "C", "B"), ending at B.
-   Finally, after five more moves, you end at 3.

So, given the actual keypad layout, the code would be 5DB3.

Using the same instructions in your puzzle input, what is the correct bathroom code?
"""

MOVES = {
    "1": {"U": "1", "D": "3", "L": "1", "R": "1"},
    "2": {"U": "2", "D": "6", "L": "2", "R": "3"},
    "3": {"U": "1", "D": "7", "L": "2", "R": "4"},
    "4": {"U": "4", "D": "8", "L": "3", "R": "4"},
    "5": {"U": "5", "D": "5", "L": "5", "R": "6"},
    "6": {"U": "2", "D": "A", "L": "5", "R": "7"},
    "7": {"U": "3", "D": "B", "L": "6", "R": "8"},
    "8": {"U": "4", "D": "C", "L": "7", "R": "9"},
    "9": {"U": "9", "D": "9", "L": "8", "R": "9"},
    "A": {"U": "6", "D": "A", "L": "A", "R": "B"},
    "B": {"U": "7", "D": "D", "L": "A", "R": "C"},
    "C": {"U": "8", "D": "C", "L": "B", "R": "C"},
    "D": {"U": "B", "D": "D", "L": "D", "R": "D"},
}


def follow(directions: str, start: str) -> int:
    current_position = start
    for turn in directions:
        current_position = MOVES[current_position][turn]
    return current_position


assert follow("ULL", "5") == "5"
assert follow("RRDDD", "5") == "D"
assert follow("LURDL", "D") == "B"
assert follow("UUUUD", "B") == "3"


with open("2016/02_bathroom_security/input.txt") as f:
    start = "5"
    codes = []

    for line in f:
        code = follow(line.strip(), start)
        start = code
        codes.append(code)

    print("".join(codes))
