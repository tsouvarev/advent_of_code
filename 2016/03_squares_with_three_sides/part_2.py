"""
Now that you've helpfully marked up their design documents,
it occurs to you that triangles are specified in groups of three vertically.
Each set of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification,
numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns,
how many of the listed triangles are possible?
"""

from itertools import batched
from re import split


def is_triangle(a, b, c) -> bool:
    return a + b > c and a + c > b and b + c > a


assert is_triangle(1, 1, 1) is True
assert is_triangle(5, 10, 25) is False


with open("2016/03_squares_with_three_sides/input.txt") as f:
    res = 0

    for lines in batched(f, 3):
        split_line = lambda l: map(int, split(r"\s+", l.strip()))  # noqa: E731
        triangles = zip(*map(split_line, lines))

        for triangle in triangles:
            if is_triangle(*triangle):
                res += 1

    print(res)
