"""
While snooping around the local network of EBHQ,
you compile a list of IP addresses (they're IPv7, of course; IPv6 is much too limited).
You'd like to figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA.
An ABBA is any four-character sequence
which consists of a pair of two different characters
followed by the reverse of that pair, such as xyyx or abba.
However, the IP also must not have an ABBA within any hypernet sequences,
which are contained by square brackets.

For example:

-   abba[mnop]qrst supports TLS (abba outside square brackets).
-   abcd[bddb]xyyx does not support TLS
    (bddb is within square brackets, even though xyyx is outside square brackets).
-   aaaa[qwer]tyui does not support TLS
    (aaaa is invalid; the interior characters must be different).
-   ioxxoj[asdfgh]zxcvbn supports TLS
    (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?
"""

from collections.abc import Iterator
from itertools import takewhile


def does_support_tls(ip: str) -> bool:
    ip_iterator = iter(ip)
    some_supernet_has_abba = False

    while True:
        supernet = _collect_net(ip_iterator, "[")
        hypernet = _collect_net(ip_iterator, "]")

        if not (supernet or hypernet):
            break

        if _check_part(hypernet):
            return False

        some_supernet_has_abba |= _check_part(supernet)

    return some_supernet_has_abba


def _collect_net(ip: list[str], stopper: str) -> list[str]:
    return list(takewhile(lambda c: c != stopper, ip))


def _check_part(part: list[str]) -> bool:
    return any(map(_has_abba, _fourwise(part)))


def _has_abba(part: list[str]) -> bool:
    a, b, c, d = part
    return a == d and b == c and a != b


def _fourwise(seq: list[str]) -> Iterator[str]:
    for i in range(len(seq) - 3):
        yield seq[i : i + 4]


assert _collect_net([], "[") == []
assert _collect_net(["a", "s", "d", "["], "[") == ["a", "s", "d"]
assert _collect_net(["a", "s", "d"], "[") == ["a", "s", "d"]

assert _check_part([]) is False
assert _check_part(["a", "b", "b", "a"]) is True
assert _check_part(["a", "s", "a", "b", "b", "a", "f", "d"]) is True

assert _has_abba(["a", "b", "b", "a"]) is True
assert _has_abba(["a", "b", "c", "a"]) is False

assert does_support_tls("abba[mnop]qrst") is True
assert does_support_tls("ab[mnop]ba") is False
assert does_support_tls("abcd[bddb]xyyx") is False
assert does_support_tls("aaaa[qwer]tyui") is False
assert does_support_tls("ioxxoj[asdfgh]zxcvbn") is True


with open("2016/07_internet_protocol_version_7/input.txt") as f:
    res = 0

    for line in f:
        if does_support_tls(line.strip()):
            res += 1

    print(res)
