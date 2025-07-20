"""
The next year, to speed up the process, Santa creates a robot version of himself,
Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location
(delivering two presents to the same starting house),
then take turns moving based on instructions from the elf,
who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:
-   ^v delivers presents to 3 houses,
    because Santa goes north, and then Robo-Santa goes south.
-   ^>v< now delivers presents to 3 houses,
    and Santa and Robo-Santa end up back where they started.
-   ^v^v^v^v^v now delivers presents to 11 houses,
    with Santa going one direction and Robo-Santa going the other.

"""

from itertools import batched


def count_deliveries(directions: str) -> int:
    seen_xy = {(0, 0)}

    for role_directions in _split_directions(directions):
        x, y = 0, 0

        for d in role_directions:
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


def _split_directions(directions: str) -> tuple[str, str]:
    return zip(*batched(directions, n=2))


assert list(_split_directions("1234")) == [("1", "3"), ("2", "4")]

assert count_deliveries("^v") == 3
assert count_deliveries("^>v<") == 3
assert count_deliveries("^v^v^v^v^v") == 11


with open("2015/03_perfectly_spherical_houses_in_a_vacuum/input.txt") as f:
    print(count_deliveries(f.read()))
