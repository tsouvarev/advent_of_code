"""
Then, you notice the instructions continue on the back of the Recruiting Document.
Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8,
the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?
"""

NEXT_DIRECTION = {
    ("U", "L"): "L",
    ("U", "R"): "R",
    ("D", "L"): "R",
    ("D", "R"): "L",
    ("L", "L"): "D",
    ("L", "R"): "U",
    ("R", "L"): "U",
    ("R", "R"): "D",
}


def follow(*directions: str) -> int:
    trackers = {"L": _track_left, "R": _track_right, "U": _track_up, "D": _track_down}

    x, y = 0, 0
    current_direction = "U"
    visited_locations = set()

    for direction in directions:
        turn, steps = _parse_direction(direction)

        next_direction = NEXT_DIRECTION[(current_direction, turn)]
        tracker = trackers[next_direction]

        for loc in tracker(x, y, steps):
            if loc in visited_locations:
                x, y = loc
                return abs(x) + abs(y)

            visited_locations.add(loc)

        x, y = loc
        current_direction = next_direction

    raise ValueError


def _parse_direction(direction: str) -> tuple[str, int]:
    return direction[0], int(direction[1:])


def _track_left(x, y, steps):
    for s in range(1, steps + 1):
        yield x - s, y


def _track_right(x, y, steps):
    for s in range(1, steps + 1):
        yield x + s, y


def _track_up(x, y, steps):
    for s in range(1, steps + 1):
        yield x, y + s


def _track_down(x, y, steps):
    for s in range(1, steps + 1):
        yield x, y - s


assert list(_track_left(0, 0, 3)) == [(-1, 0), (-2, 0), (-3, 0)]
assert list(_track_right(0, 0, 3)) == [(1, 0), (2, 0), (3, 0)]
assert list(_track_up(0, 0, 3)) == [(0, 1), (0, 2), (0, 3)]
assert list(_track_down(0, 0, 3)) == [(0, -1), (0, -2), (0, -3)]

assert follow("R8", "R4", "R4", "R8") == 4


with open("2016/01_no_time_for_a_taxicab/input.txt") as f:
    print(follow(*f.read().strip().split(", ")))
