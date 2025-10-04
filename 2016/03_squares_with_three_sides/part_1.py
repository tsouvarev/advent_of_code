"""
Now that you can think clearly,
you move deeper into the labyrinth of hallways and office furniture
that makes up this part of Easter Bunny HQ.
This must be a graphic design department;
the walls are covered in specifications for triangles.

Or are they?

The design document gives the side lengths of each triangle it describes,
but... 5 10 25? Some of these aren't triangles.
You can't help but mark the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining side.
For example, the "triangle" given above is impossible,
because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?
"""

from re import split


def is_triangle(a, b, c) -> bool:
    return a + b > c and a + c > b and b + c > a


assert is_triangle(1, 1, 1) is True
assert is_triangle(5, 10, 25) is False


with open("2016/03_squares_with_three_sides/input.txt") as f:
    res = 0

    for line in f:
        a, b, c = map(int, split(r"\s+", line.strip()))
        if is_triangle(a, b, c):
            res += 1

    print(res)
