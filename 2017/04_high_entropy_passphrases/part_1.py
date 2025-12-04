"""
A new system policy has been put in place
that requires all accounts to use a passphrase instead of simply a password.
A passphrase consists of a series of words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:

- aa bb cc dd ee is valid.
- aa bb cc dd aa is not valid - the word aa appears more than once.
- aa bb cc dd aaa is valid - aa and aaa count as different words.

The system's full passphrase list is available as your puzzle input.
How many passphrases are valid?
"""

from collections import Counter


def is_valid(passphrase: str) -> bool:
    word_counts = Counter(passphrase.split(" "))
    _, count = word_counts.most_common(1)[0]
    return count < 2


assert is_valid("aa bb cc dd ee") is True
assert is_valid("aa bb cc dd aa") is False
assert is_valid("aa bb cc dd aaa") is True


with open("2017/04_high_entropy_passphrases/input.txt") as f:
    passphrases = [line.strip() for line in f]
    print(sum(map(is_valid, passphrases)))
