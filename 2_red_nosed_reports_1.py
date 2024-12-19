"""
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian,
the engineers there run up to you as soon as they see you.
Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help
analyzing some unusual data from the Red-Nosed reactor.
You turn to check if The Historians are waiting for you,
but they seem to have already divided into groups that are currently searching every corner of the facility.
You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line.
Each report is a list of numbers called levels that are separated by spaces. For example:
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9

This example data contains six reports each containing five levels.
The engineers are trying to figure out which reports are safe.
The Red-Nosed reactor safety systems can only tolerate levels
that are either gradually increasing or gradually decreasing.

So, a report only counts as safe if both of the following are true:
- The levels are either all increasing or all decreasing.
- Any two adjacent levels differ by at least one and at most three.

In the example above, the reports can be found safe or unsafe by checking those rules:
- 7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
- 1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
- 9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
- 1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
- 8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
- 1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.

So, in this example, 2 reports are safe.
Analyze the unusual data from the engineers. How many reports are safe?
"""

from itertools import starmap
from functools import reduce


def is_report_safe(report: list) -> bool:
    direction = report[0] > report[1]
    return all(
        starmap(_all_fn(_has_ok_diff, _has_direction(direction)), _pairwise(report))
    )


def _has_ok_diff(a, b):
    return 1 <= abs(a - b) <= 3


def _has_direction(direction):
    return lambda a, b: (a > b) == direction


def _all_fn(*fns):
    return lambda *args, **kwargs: all(fn(*args, **kwargs) for fn in fns)


def _pairwise(seq):
    x, y = iter(seq), iter(seq)
    next(y)
    return zip(x, y)


assert is_report_safe([7, 6, 4, 2, 1]) is True
assert is_report_safe([1, 2, 7, 8, 9]) is False
assert is_report_safe([9, 7, 6, 2, 1]) is False
assert is_report_safe([1, 3, 2, 4, 5]) is False
assert is_report_safe([8, 6, 4, 4, 1]) is False
assert is_report_safe([1, 3, 6, 7, 9]) is True

with open("2_red_nosed_reports_input.txt") as f:
    reports = []
    for l in f:
        raw_report = l.split(" ")
        reports.append(list(map(int, raw_report)))

    print(len([r for r in reports if is_report_safe(r)]))
