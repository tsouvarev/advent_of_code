"""
How many IPs are allowed by the blacklist?
"""

from typing import NamedTuple

from parse import parse


class Rule(NamedTuple):
    low: int
    high: int


def solve(rules: list[Rule], max_ip: int) -> int:
    highest = 0
    num_allowed_ips = 0

    for rule in sorted(rules):
        if highest + 1 < rule.low:
            num_allowed_ips += rule.low - highest - 1
        highest = max(highest, rule.high)

    return num_allowed_ips + (max_ip - highest)


rules = [Rule(0, 2), Rule(4, 7), Rule(5, 8)]
assert solve(rules, 9) == 2

rules = [Rule(0, 5), Rule(4, 7), Rule(5, 8)]
assert solve(rules, 9) == 1


with open("2016/20_firewall_rules/input.txt") as f:
    rules = []
    for line in f:
        rules.append(Rule(*parse("{:d}-{:d}", line.strip()).fixed))

    print(solve(rules, 4_294_967_295))
