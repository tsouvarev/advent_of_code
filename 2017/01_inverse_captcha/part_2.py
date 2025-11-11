"""
You notice a progress bar that jumps to 50% completion.
Apparently, the door isn't yet satisfied, but it did emit a star as encouragement.

The instructions change:
Now, instead of considering the next digit,
it wants you to consider the digit halfway around the circular list.
That is, if your list contains 10 items, only include a digit in your sum
if the digit 10/2 = 5 steps forward matches it.
Fortunately, your list has an even number of elements.

For example:

-   1212 produces 6: the list contains 4 items,
    and all four digits match the digit 2 items ahead.
-   1221 produces 0, because every comparison is between a 1 and a 2.
-   123425 produces 4, because both 2s match each other, but no other digit has a match.
-   123123 produces 12.
-   12131415 produces 4.

What is the solution to your new captcha?
"""


def solve(captcha: str) -> tuple[int, list[int]]:
    matches = []
    half = len(captcha) // 2

    for i, c in enumerate(captcha):
        offset = (i + half) % len(captcha)
        if c == captcha[offset]:
            matches.append(int(c))

    return sum(matches), matches


assert solve("1212") == (6, [1, 2, 1, 2])
assert solve("1221") == (0, [])
assert solve("123425") == (4, [2, 2])
assert solve("123123") == (12, [1, 2, 3, 1, 2, 3])
assert solve("12131415") == (4, [1, 1, 1, 1])


with open("2017/01_inverse_captcha/input.txt") as f:
    print(solve(f.read()))
