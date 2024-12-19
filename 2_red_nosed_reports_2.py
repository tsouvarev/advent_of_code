"""
The engineers are surprised by the low number of safe reports
until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module
that lets the reactor safety systems tolerate
a single bad level in what would otherwise be a safe report.
It's like the bad level never happened!

Now, the same rules apply as before,
except if removing a single level from an unsafe report would make it safe,
the report instead counts as safe.

More of the above example's reports are now safe:
- 7 6 4 2 1: Safe without removing any level.
- 1 2 7 8 9: Unsafe regardless of which level is removed.
- 9 7 6 2 1: Unsafe regardless of which level is removed.
- 1 3 2 4 5: Safe by removing the second level, 3.
- 8 6 4 4 1: Safe by removing the third level, 4.
- 1 3 6 7 9: Safe without removing any level.

Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations
where the Problem Dampener can remove a single level from unsafe reports.
How many reports are now safe?
"""

from itertools import pairwise


def is_report_safe(report: list, *, allow_fix=True) -> bool:
    direction = _get_dominant_direction(report)

    for i in range(len(report) - 1):
        a, b = report[i], report[i + 1]

        if _has_ok_diff(a, b) and _has_direction(direction, a, b):
            continue

        if not allow_fix:
            return False

        without_a, without_b = report.copy(), report.copy()
        without_a.pop(i)
        without_b.pop(i + 1)

        return is_report_safe(without_a, allow_fix=False) or is_report_safe(
            without_b,
            allow_fix=False,
        )

    return True


def _has_ok_diff(a, b):
    return 1 <= abs(a - b) <= 3


def _get_dominant_direction(seq):
    direction = sum(a > b for a, b in pairwise(seq))
    return direction > len(seq) / 2


def _has_direction(direction, a, b):
    return (a > b) == direction


assert is_report_safe([7, 6, 4, 2, 1]) is True
assert is_report_safe([1, 2, 7, 8, 9]) is False
assert is_report_safe([9, 7, 6, 2, 1]) is False
assert is_report_safe([1, 3, 2, 4, 5]) is True
assert is_report_safe([8, 6, 4, 4, 1]) is True
assert is_report_safe([1, 3, 6, 7, 9]) is True
assert is_report_safe([25, 24, 25, 27, 30, 32]) is True
assert is_report_safe([38, 40, 39, 38, 37, 34]) is True
assert is_report_safe([69, 72, 69, 67, 66, 63, 62]) is True

with open("2_red_nosed_reports_input.txt") as f:
    reports = []
    for l in f:
        raw_report = l.split(" ")
        reports.append(list(map(int, raw_report)))

    safe_reports = {tuple(r) for r in reports if is_report_safe(r)}
    print(len(safe_reports))
