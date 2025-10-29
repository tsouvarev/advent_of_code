"""
Of course, in order to make this process even more secure,
you've also implemented key stretching.

Key stretching forces attackers to spend more time generating hashes.
Unfortunately, it forces everyone else to spend more time, too.

To implement key stretching, whenever you generate a hash, before you use it,
you first find the MD5 hash of that hash, then the MD5 hash of that hash, and so on,
a total of 2016 additional hashings.
Always use lowercase hexadecimal representations of hashes.

For example, to find the stretched hash for index 0 and salt abc:

- Find the MD5 hash of abc0: 577571be4de9dcce85a041ba0410f29f.
- Then, find the MD5 hash of that hash: eec80a0c92dc8a0777c619d9bb51e910.
- Then, find the MD5 hash of that hash: 16062ce768787384c81fe17a7a60c7e3.
- ...repeat many times...
- Then, find the MD5 hash of that hash: a107ff634856bb300138cac6568c0f24.

So, the stretched hash for index 0 in this situation is a107ff....
In the end, you find the original hash (one use of MD5),
then find the hash-of-the-previous-hash 2016 times, for a total of 2017 uses of MD5.

The rest of the process remains the same, but now the keys are entirely different.
Again for salt abc:

-   The first triple (222, at index 5)
    has no matching 22222 in the next thousand hashes.
-   The second triple (eee, at index 10) hash a matching eeeee at index 89,
    and so it is the first key.
-   Eventually, index 22551 produces the 64th key
    (triple fff with matching fffff at index 22859).

Given the actual salt in your puzzle input
and using 2016 extra MD5 calls of key stretching,
what index now produces your 64th one-time pad key?
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
    hashed = f"{salt}{i}"
    for _ in range(2017):
        hashed = md5(hashed.encode()).hexdigest().lower()  # noqa: S324
    return hashed


assert _get_repeater("123333344") == "3"
assert _get_repeater("1234") is None
assert _get_repeater("111122223333433333") == "1"

assert _is_candidate_follower("1233333", "3") is True
assert _is_candidate_follower("1233333", "4") is False

assert list(islice(generate_keys("abc"), 2)) == [10, 25]
assert list(islice(generate_keys("abc"), 64))[-1] == 22551


for i, index in enumerate(generate_keys("ihaygndm"), 1):
    print(i, index)
    if i == 64:
        break
