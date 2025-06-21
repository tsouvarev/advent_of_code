"""
Another push of the button leaves you
in the familiar hallways of some friendly amphipods!
Good thing you each somehow got your own personal mini submarine.
The Historians jet away in search of the Chief, mostly by driving directly into walls.

While The Historians quickly figure out how to pilot these things,
you notice an amphipod in the corner struggling with his computer.
He's trying to make more contiguous free space by compacting all of the files,
but his program isn't working; you offer to help.

He shows you the disk map (your puzzle input) he's already generated. For example:

2333133121414131402

The disk map uses a dense format
to represent the layout of files and free space on the disk.
The digits alternate between indicating the length of a file
and the length of free space.

So, a disk map like 12345 would represent a one-block file, two blocks of free space,
a three-block file, four blocks of free space, and then a five-block file.
A disk map like 90909 would represent three nine-block files in a row
(with no free space between them).

Each file on disk also has an ID number based on the order of the files
as they appear before they are rearranged, starting with ID 0.
So, the disk map 12345 has three files:
a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2.
Using one character for each block where digits are the file ID and . is free space,
the disk map 12345 represents these individual blocks:

0..111....22222

The first example above, 2333133121414131402, represents these individual blocks:

00...111...2...333.44.5555.6666.777.888899

The amphipod would like to move file blocks one at a time
from the end of the disk to the leftmost free space block
(until there are no gaps remaining between file blocks).
For the disk map 12345, the process looks like this:

0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......

The first example requires a few more steps:

00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566..............

The final step of this file-compacting process is to update the filesystem checksum.
To calculate the checksum, add up the result of multiplying each of these blocks' position
with the file ID number it contains.
The leftmost block is in position 0. If a block contains free space, skip it instead.

Continuing the first example,
the first few blocks' position multiplied by its file ID number are
0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on.
In this example, the checksum is the sum of these, 1928.

Compact the amphipod's hard drive using the process he requested.
What is the resulting filesystem checksum?
"""

from itertools import count
from typing import NamedTuple

type DiskMap = list[Cell]


class Cell(NamedTuple):
    id: int | None

    @property
    def is_empty(self):
        return self.id is None


def defragment(disk_map: DiskMap) -> DiskMap:
    curr_pos, shift_pos = 0, len(disk_map) - 1

    while _has_cells(disk_map[curr_pos:]):
        curr_cell = disk_map[curr_pos]

        if curr_cell.is_empty:
            while disk_map[shift_pos].is_empty:
                shift_pos -= 1

            _swap_cells(disk_map, curr_pos, shift_pos)
            shift_pos -= 1

        curr_pos += 1

    return _strip_disk_map(disk_map)


def checksum(disk_map: DiskMap) -> int:
    return sum(i * c.id for i, c in enumerate(disk_map))


def _has_cells(disk_map: DiskMap) -> bool:
    return any(c.id is not None for c in disk_map)


def _swap_cells(disk_map: DiskMap, from_: int, to_: int) -> bool:
    disk_map[from_], disk_map[to_] = disk_map[to_], disk_map[from_]


def _strip_disk_map(disk_map: DiskMap) -> DiskMap:
    for i, c in enumerate(disk_map):
        if c.is_empty:
            return disk_map[:i]
    return disk_map


def _to_str(disk_map: DiskMap) -> str:
    return "".join(str("." if c.is_empty else c.id) for c in disk_map)


def _to_array(s: str) -> DiskMap:
    is_file = True
    res = []
    id_generator = count()

    for length in s:
        new_id = next(id_generator) if is_file else None
        res.extend([Cell(id=new_id)] * int(length))
        is_file = not is_file

    return res


def _to_array_from_ids(s: str) -> DiskMap:
    return [Cell(id=int(new_id)) for new_id in s]


def _pp_defragment(s):
    return _to_str(defragment(_to_array(s)))


assert _to_array("111") == [Cell(id=0), Cell(id=None), Cell(id=1)]
assert _to_str(_to_array("12345")) == "0..111....22222"

assert _pp_defragment("12345") == "022111222"
assert _pp_defragment("2333133121414131402") == "0099811188827773336446555566"

assert checksum(_to_array_from_ids("022111222")) == 60
assert checksum(_to_array_from_ids("0099811188827773336446555566")) == 1928


with open("9_disk_fragmenter/input.txt") as f:
    print(checksum(defragment(_to_array(f.readline().strip()))))
