"""
You are faced with a security door designed by Easter Bunny engineers
that seem to have acquired most of their security knowledge by watching hacking movies.

The eight-character password for the door is generated one character at a time
by finding the MD5 hash of some Door ID (your puzzle input)
and an increasing integer index (starting with 0).

A hash indicates the next character in the password
if its hexadecimal representation starts with five zeroes.
If it does, the sixth character in the hash is the next character of the password.

For example, if the Door ID is abc:

-   The first index which produces a hash that starts with five zeroes is 3231929,
    which we find by hashing abc3231929; the sixth character of the hash,
    and thus the first character of the password, is 1.
-   5017308 produces the next interesting hash, which starts with 000008f82...,
    so the second character of the password is 8.
-   The third time a hash starts with five zeroes is for abc5278568,
    discovering the character f.

In this example, after continuing this search a total of eight times,
the password is 18f47a30.

Given the actual Door ID, what is the password?
"""

from collections.abc import Iterator
from hashlib import md5
from itertools import count, islice


def hack(door_id: str) -> str:
    return "".join(islice(_generate_password(door_id), 8))


def _generate_password(door_id: str) -> Iterator[str]:
    for i in count(1):
        digest = md5(f"{door_id}{i}".encode()).hexdigest()  # noqa: S324
        if digest.startswith("00000"):
            yield digest[5]


assert hack("abc") == "18f47a30"


print(hack("abbhdwsy"))
