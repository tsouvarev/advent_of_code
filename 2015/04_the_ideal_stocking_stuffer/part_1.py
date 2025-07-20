"""
Santa needs help mining some AdventCoins (very similar to bitcoins)
to use as gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal,
start with at least five zeroes.
The input to the MD5 hash is some secret key (your puzzle input, given below)
followed by a number in decimal.
To mine AdventCoins, you must find Santa the lowest positive number
(no leading zeroes: 1, 2, 3, ...) that produces such a hash.

For example:
-   If your secret key is abcdef, the answer is 609043,
    because the MD5 hash of abcdef609043 starts with five zeroes (000001dbbfa...),
    and it is the lowest such number to do so.
-   If your secret key is pqrstuv, the lowest number it combines with
    to make an MD5 hash starting with five zeroes is 1048970;
    that is, the MD5 hash of pqrstuv1048970 looks like 000006136ef....

Your puzzle input is yzbqklnj.
"""

from hashlib import md5
from itertools import count


def find_lowest_hash(input_str: str):
    for i in count(1):
        hashed = md5(f"{input_str}{i}".encode())  # noqa: S324

        if hashed.hexdigest().startswith("00000"):
            return i
    return None


assert find_lowest_hash("abcdef") == 609043
assert find_lowest_hash("pqrstuv") == 1048970


print(find_lowest_hash("yzbqklnj"))
