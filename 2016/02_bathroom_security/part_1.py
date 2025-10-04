"""
You arrive at Easter Bunny Headquarters under cover of darkness.
However, you left in such a rush that you forgot to use the bathroom!
Fancy office buildings like this one usually have keypad locks on their bathrooms,
so you search the front desk for the code.

"In order to improve security," the document you find says,
"bathroom codes will no longer be written down.
Instead, please memorize and follow the procedure below to access the bathrooms."

The document goes on to explain that each button to be pressed
can be found by starting on the previous button
and moving to adjacent buttons on the keypad:
U moves up, D moves down, L moves left, and R moves right.
Each line of instructions corresponds to one button,
starting at the previous button (or, for the first line, the "5" button);
press whatever button you're on at the end of each line.
If a move doesn't lead to a button, ignore it.

You can't hold it much longer,
so you decide to figure out the code as you walk to the bathroom.
You picture a keypad like this:

1 2 3
4 5 6
7 8 9

Suppose your instructions are:

ULL
RRDDD
LURDL
UUUUD

-   You start at "5" and move up (to "2"), left (to "1"),
    and left (you can't, and stay on "1"), so the first button is 1.
-   Starting from the previous button ("1"), you move right twice (to "3")
    and then down three times (stopping at "9" after two moves and ignoring the third),
    ending up with 9.
-   Continuing from "9", you move left, up, right, down, and left, ending with 8.
-   Finally, you move up four times (stopping at "2"), then down once, ending with 5.

So, in this example, the bathroom code is 1985.

Your puzzle input is the instructions from the document you found at the front desk.
What is the bathroom code?
"""

MOVES = {
    1: {"U": 1, "D": 4, "L": 1, "R": 2},
    2: {"U": 2, "D": 5, "L": 1, "R": 3},
    3: {"U": 3, "D": 6, "L": 2, "R": 3},
    4: {"U": 1, "D": 7, "L": 4, "R": 5},
    5: {"U": 2, "D": 8, "L": 4, "R": 6},
    6: {"U": 3, "D": 9, "L": 5, "R": 6},
    7: {"U": 4, "D": 7, "L": 7, "R": 8},
    8: {"U": 5, "D": 8, "L": 7, "R": 8},
    9: {"U": 6, "D": 9, "L": 8, "R": 9},
}


def follow(directions: str, start: int) -> int:
    current_position = start
    for turn in directions:
        current_position = MOVES[current_position][turn]
    return current_position


assert follow("ULL", 5) == 1
assert follow("RRDDD", 1) == 9
assert follow("LURDL", 9) == 8
assert follow("UUUUD", 8) == 5


with open("2016/02_bathroom_security/input.txt") as f:
    start = 5
    codes = []

    for line in f:
        code = follow(line.strip(), start)
        start = code
        codes.append(str(code))

    print("".join(codes))
