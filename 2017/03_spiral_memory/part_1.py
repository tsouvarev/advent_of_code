"""
You come across an experimental new kind of memory
stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern
starting at a location marked 1 and then counting up while spiraling outward.
For example, the first few squares are allocated like this:

37  36  35  34  33  32  31
38  17  16  15  14  13  30  55
39  18   5   4   3  12  29  54
40  19   6   1   2  11  28  53
41  20   7   8   9  10  27  52
41  21  22  23  24  25  26  51
43  44  45  46  47  48  49  50

While this is very space-efficient (no squares are skipped),
requested data must be carried back to square 1
(the location of the only access port for this memory system)
by programs that can only move up, down, left, or right.
They always take the shortest path:
the Manhattan Distance between the location of the data and square 1.

For example:

- Data from square 1 is carried 0 steps, since it's at the access port.
- Data from square 12 is carried 3 steps, such as: down, left, left.
- Data from square 23 is carried only 2 steps: up twice.
- Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data
from the square identified in your puzzle input all the way to the access port?
"""

from itertools import count


def solve(square: int) -> int:
    for circle in count(1):
        side = (circle - 1) * 2 + 1
        if side**2 > square:
            break

    radials = [side**2 - (side - 1) / 2 - i * (side - 1) for i in range(4)]
    steps_to_radial = min(abs(square - radial) for radial in radials)

    return steps_to_radial + circle - 1


assert solve(12) == 3
assert solve(23) == 2
assert solve(1024) == 31

print(solve(277_678))
