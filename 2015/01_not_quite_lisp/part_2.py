"""
Now, given the same instructions, find the position
of the first character that causes him to enter the basement (floor -1).
The first character in the instructions has position 1,
the second character has position 2, and so on.

For example:

    ) causes him to enter the basement at character position 1.
    ()()) causes him to enter the basement at character position 5.

What is the position of the character that causes Santa to first enter the basement?
"""


def move_santa_at_basement(instructions: str) -> int:
    floor = 0

    for i, c in enumerate(instructions):
        match c:
            case "(":
                floor += 1
            case ")":
                floor -= 1

        if floor == -1:
            return i + 1

    return -1


assert move_santa_at_basement(")") == 1
assert move_santa_at_basement("()())") == 5
assert move_santa_at_basement("(())") == -1
assert move_santa_at_basement("()()") == -1
assert move_santa_at_basement("(((") == -1
assert move_santa_at_basement("(()(()(") == -1
assert move_santa_at_basement("))(((((") == 1
assert move_santa_at_basement("())") == 3
assert move_santa_at_basement("))(") == 1
assert move_santa_at_basement(")))") == 1
assert move_santa_at_basement(")())())") == 1


with open("2015/01_not_quite_lisp/input.txt") as f:
    print(move_santa_at_basement(f.read()))
