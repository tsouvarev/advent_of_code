"""
Now find one that starts with six zeroes.
"""

from hashlib import md5
from itertools import batched, count, islice
from multiprocessing import Pool

POOL_SIZE = 100


def find_lowest_hash(input_str: str):
    with Pool(POOL_SIZE) as p:
        for batch in batched(_get_ranges(input_str), n=POOL_SIZE):
            res = list(filter(bool, p.map(_check_hash, batch)))
            if any(res):
                return res[0]
    return None


def _get_ranges(input_str):
    start, step = 0, 10_000

    while True:
        yield input_str, start, start + step - 1
        start += step


def _check_hash(*args):
    input_str, start, finish = args[0]

    for i in count(start):
        hashed = md5(f"{input_str}{i}".encode())  # noqa: S324

        if hashed.hexdigest().startswith("000000"):
            return i

        if i == finish:
            return None
    return None


assert list(islice(_get_ranges("a"), 2)) == [("a", 0, 9_999), ("a", 10_000, 19_999)]


assert find_lowest_hash("abcdef") == 6742839
assert find_lowest_hash("pqrstuv") == 5714438


print(find_lowest_hash("yzbqklnj"))
