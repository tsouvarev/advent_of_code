"""
In order to communicate securely with Santa while you're on this mission,
you've been using a one-time pad that you generate using a pre-agreed algorithm.
Unfortunately, you've run out of keys in your one-time pad,
and so you need to generate some more.

To generate keys, you first get a stream of random data
by taking the MD5 of a pre-arranged salt (your puzzle input)
and an increasing integer index (starting with 0, and represented in decimal);
the resulting MD5 hash should be represented
as a string of lowercase hexadecimal digits.

However, not all of these MD5 hashes are keys,
and you need 64 new keys for your one-time pad. A hash is a key only if:

-   It contains three of the same character in a row, like 777.
    Only consider the first such triplet in a hash.
-   One of the next 1000 hashes in the stream contains that same character
    five times in a row, like 77777.

Considering future hashes for five-of-a-kind sequences
does not cause those hashes to be skipped;
instead, regardless of whether the current hash is a key,
always resume testing for keys starting with the very next hash.

For example, if the pre-arranged salt is abc:

-   The first index which produces a triple is 18,
    because the MD5 hash of abc18 contains ...cc38887a5....
    However, index 18 does not count as a key for your one-time pad,
    because none of the next thousand hashes (index 19 through index 1018)
    contain 88888.
-   The next index which produces a triple is 39; the hash of abc39 contains eee.
    It is also the first key: one of the next thousand hashes
    (the one at index 816) contains eeeee.
-   None of the next six triples are keys, but the one after that, at index 92,
    is: it contains 999 and index 200 contains 99999.
-   Eventually, index 22728 meets all of the criteria to generate the 64th key.

So, using our example salt of abc, index 22728 produces the 64th key.

Given the actual salt in your puzzle input,
what index produces your 64th one-time pad key?
"""

from collections.abc import Iterator
from functools import cache
from hashlib import md5
from itertools import count, islice
from re import findall


def generate_keys(salt: str) -> Iterator[int]:
    for i in count(1):
        key_candidate = _gen_hash(salt, i)

        repeater = _get_repeater(key_candidate)
        if not repeater:
            continue

        for j in range(1000):
            hash_to_check = _gen_hash(salt, i + j + 1)

            if _is_candidate_follower(hash_to_check, repeater):
                yield i
                break


def _get_repeater(h: str) -> str | None:
    repeats = findall(r"(\w)\1{2}", h)
    if not repeats:
        return None
    return repeats[0]


def _is_candidate_follower(h: str, repeater: str) -> bool:
    return bool(findall(rf"{repeater}{{5}}", h))


@cache
def _gen_hash(salt: str, i: int) -> str:
    return md5(f"{salt}{i}".encode()).hexdigest().lower()  # noqa: S324


assert _get_repeater("123333344") == "3"
assert _get_repeater("1234") is None
assert _get_repeater("111122223333433333") == "1"

assert _is_candidate_follower("1233333", "3") is True
assert _is_candidate_follower("1233333", "4") is False

assert list(islice(generate_keys("abc"), 2)) == [39, 92]
assert list(islice(generate_keys("abc"), 64))[-1] == 22728


print(list(islice(generate_keys("ihaygndm"), 64))[-1])
