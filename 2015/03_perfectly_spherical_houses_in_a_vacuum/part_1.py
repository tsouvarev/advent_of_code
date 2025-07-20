"""
Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location,
and then an elf at the North Pole calls him via radio and tells him where to move next.
Moves are always exactly one house to the north (^), south (v), east (>), or west (<).
After each move, he delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much eggnog,
and so his directions are a little off,
and Santa ends up visiting some houses more than once.

How many houses receive at least one present?

For example:
-   > delivers presents to 2 houses: one at the starting location, and one to the east.
-   ^>v< delivers presents to 4 houses in a square,
    including twice to the house at his starting/ending location.
-   ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses
"""


def count_deliveries(directions: str) -> int:
    x, y = 0, 0
    seen_xy = {(0, 0)}

    for d in directions:
        match d:
            case "^":
                x += 1
            case "v":
                x -= 1
            case ">":
                y += 1
            case "<":
                y -= 1

        seen_xy.add((x, y))

    return len(seen_xy)


assert count_deliveries(">") == 2
assert count_deliveries("^>v<") == 4
assert count_deliveries("^v^v^v^v^v") == 2


with open("2015/03_perfectly_spherical_houses_in_a_vacuum/input.txt") as f:
    print(count_deliveries(f.read()))
