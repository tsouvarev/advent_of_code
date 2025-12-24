"""
As you enter this room, you hear a loud click!
Some of the tiles in the floor here seem to be pressure plates for traps,
and the trap you just triggered has run out of... whatever it tried to do to you.
You doubt you'll be so lucky next time.

Upon closer examination, the traps and safe tiles in this room seem to follow a pattern.
The tiles are arranged into rows that are all the same width;
you take note of the safe tiles (.) and traps (^) in the first row (your puzzle input).

The type of tile (trapped or safe) in each row
is based on the types of the tiles in the same position,
and to either side of that position, in the previous row.
(If either side is off either end of the row,
 it counts as "safe" because there isn't a trap embedded in the wall.)

For example, suppose you know the first row (with tiles marked by letters)
and want to determine the next row (with tiles marked by numbers):

ABCDE
12345

The type of tile 2 is based on the types of tiles A, B, and C;
the type of tile 5 is based on tiles D, E, and an imaginary "safe" tile.
Let's call these three tiles from the previous row
the left, center, and right tiles, respectively.
Then, a new tile is a trap only in one of the following situations:

- Its left and center tiles are traps, but its right tile is not.
- Its center and right tiles are traps, but its left tile is not.
- Only its left tile is a trap.
- Only its right tile is a trap.

In any other situation, the new tile is safe.

Then, starting with the row ..^^.,
you can determine the next row by applying those rules to each new tile:

-   The leftmost character on the next row considers the left
    (nonexistent, so we assume "safe"), center (the first ., which means "safe"),
    and right (the second ., also "safe") tiles on the previous row.
    Because all of the trap rules require
    a trap in at least one of the previous three tiles,
    the first tile on this new row is also safe, ..
-   The second character on the next row considers its
    left (.), center (.), and right (^) tiles from the previous row.
    This matches the fourth rule: only the right tile is a trap.
    Therefore, the next tile in this new row is a trap, ^.
-   The third character considers .^^,
    which matches the second trap rule: its center and right tiles are traps,
    but its left tile is not. Therefore, this tile is also a trap, ^.
-   The last two characters in this new row match
    the first and third rules, respectively, and so they are both also traps, ^.

After these steps, we now know the next row of tiles in the room: .^^^^.
Then, we continue on to the next row, using the same rules, and get ^^..^.
After determining two new rows, our map looks like this:

..^^.
.^^^^
^^..^

Here's a larger example with ten tiles per row and ten rows:

.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^

In ten rows, this larger example has 38 safe tiles.

Starting with the map in your puzzle input,
in a total of 40 rows (including the starting row), how many safe tiles are there?

How many safe tiles are there in a total of 400_000 rows?
"""

from collections.abc import Iterator
from itertools import islice

type Field = list[Row]
type Row = list[str]
type Cell = str
type Triplet = tuple[Cell, Cell, Cell]

SAFE, TRAP = ".^"


def gen_rows(row: Row) -> Iterator[Row]:
    yield row

    while True:
        next_row = list(map(_determine_cell, _triplets([SAFE, *row, SAFE])))
        yield next_row
        row = next_row


def _determine_cell(prev_row: Triplet) -> Cell:
    trap_cells = {
        (TRAP, TRAP, SAFE),
        (SAFE, TRAP, TRAP),
        (TRAP, SAFE, SAFE),
        (SAFE, SAFE, TRAP),
    }
    if prev_row in trap_cells:
        return TRAP
    return SAFE


def _count_safe_tiles(field: Field) -> int:
    return sum(row.count(SAFE) for row in field)


def _triplets(seq: Row) -> Iterator[Triplet]:
    first, second, third = map(iter, [seq] * 3)
    next(second)
    next(third)
    next(third)
    return zip(first, second, third)


def _to_field(raw_field: list[str]) -> Field:
    return [list(row) for row in raw_field]


assert _count_safe_tiles([*".^^.^.^^^^"]) == 3

assert _determine_cell(tuple("^^.")) is TRAP
assert _determine_cell(tuple(".^^")) is TRAP
assert _determine_cell(tuple("^..")) is TRAP
assert _determine_cell(tuple("..^")) is TRAP
assert _determine_cell(tuple("...")) is SAFE
assert _determine_cell(tuple("^^^")) is SAFE

assert list(_triplets(list("abc"))) == [("a", "b", "c")]
assert list(_triplets(list("abcd"))) == [("a", "b", "c"), ("b", "c", "d")]

assert list(islice(gen_rows(list("..^^.")), 3)) == _to_field(
    ["..^^.", ".^^^^", "^^..^"],
)
assert list(islice(gen_rows(list(".^^.^.^^^^")), 10)) == _to_field(
    [
        ".^^.^.^^^^",
        "^^^...^..^",
        "^.^^.^.^^.",
        "..^^...^^^",
        ".^^^^.^^.^",
        "^^..^.^^..",
        "^^^^..^^^.",
        "^..^^^^.^^",
        ".^^^..^.^^",
        "^^.^^^..^^",
    ],
)

with open("2016/18_like_a_rogue/input.txt") as f:
    row = list(f.read().strip())

    rows = islice(gen_rows(row), 40)
    print(sum(map(_count_safe_tiles, rows)))  # type: ignore[invalid-argument-type]

    rows = islice(gen_rows(row), 400_000)
    print(sum(map(_count_safe_tiles, rows)))  # type: ignore[invalid-argument-type]
