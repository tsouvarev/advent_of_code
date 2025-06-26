"""
The Historians sure are taking a long time.
To be fair, the infinite corridors are very large.

How many stones would you have after blinking a total of 75 times?
"""

from collections import defaultdict


def blink(*stones: int, n: int = 1) -> dict[int, int]:
    cached_stones = defaultdict(int).fromkeys(stones, 1)
    for _i in range(n):
        cached_stones = _update_stones(cached_stones)
    return cached_stones


def _update_stones(stones: dict[int, int]) -> dict[int, int]:
    cached_stones = defaultdict(int)

    for s, n in stones.items():
        if s == 0:
            cached_stones[1] += n
            continue

        num_of_digits = len(str(s))

        if num_of_digits % 2 == 0:
            half = num_of_digits // 2
            cached_stones[s // 10**half] += n
            cached_stones[s % 10**half] += n
        else:
            cached_stones[s * 2024] += n

    return cached_stones


assert blink(0) == {1: 1}
assert blink(12) == {1: 1, 2: 1}
assert blink(1000) == {10: 1, 0: 1}
assert blink(1) == {2024: 1}

assert sum(blink(125, 17, n=25).values()) == 55312

print(sum(blink(0, 89741, 316108, 7641, 756, 9, 7832357, 91, n=75).values()))
