"""
As the door slides open, you are presented with a second door
that uses a slightly more inspired security mechanism.
Clearly unimpressed by the last version
(in what movie is the password decrypted in order?!),
the Easter Bunny engineers have worked out a better solution.

Instead of simply filling in the password from left to right,
the hash now also indicates the position within the password to fill.
You still look for hashes that begin with five zeroes;
however, now, the sixth character represents the position (0-7),
and the seventh character is the character to put in that position.

A hash result of 000001f means that f is the second character in the password.
Use only the first result for each position, and ignore invalid positions.

For example, if the Door ID is abc:

-   The first interesting hash is from abc3231929, which produces 0000015...;
    so, 5 goes in position 1: _5______.
-   In the previous method, 5017308 produced an interesting hash;
    however, it is ignored, because it specifies an invalid position (8).
-   The second interesting hash is at index 5357525, which produces 000004e...;
    so, e goes in position 4: _5__e___.

You almost choke on your popcorn as the final character falls into place,
producing the password 05ace8e3.

Given the actual Door ID and this new method, what is the password?
Be extra proud of your solution if it uses a cinematic "decrypting" animation.
"""

from hashlib import md5
from itertools import count


def hack(door_id: str) -> str:
    password = ["_"] * 8
    start = 1

    while "_" in password:
        start, pos, c = _next_password_char(door_id, start + 1)

        if pos >= len(password) or password[pos] != "_":
            continue

        password[pos] = c
        print("".join(password))

    return "".join(password)


def _next_password_char(door_id: str, start: int) -> tuple[int, int, str]:
    for i in count(start):
        digest = md5(f"{door_id}{i}".encode()).hexdigest()  # noqa: S324

        match list(digest):
            case ["0", "0", "0", "0", "0", pos, c, *_]:
                return i, int(pos, base=16), c

    raise ValueError


assert hack("abc") == "05ace8e3"


print(hack("abbhdwsy"))
