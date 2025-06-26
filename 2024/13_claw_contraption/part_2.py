"""
As you go to win the first prize,
you discover that the claw is nowhere near where you expected it would be.
Due to a unit conversion error in your measurements,
the position of every prize is actually 10000000000000 higher on both the X and Y axis!

Add 10000000000000 to the X and Y position of every prize.
After making this change, the example above would now look like this:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279

Now, it is only possible to win a prize on the second and fourth claw machines.
Unfortunately, it will take many more than 100 presses to do so.

Using the corrected prize coordinates, figure out how to win as many prizes as possible.
What is the fewest tokens you would have to spend to win all possible prizes?
"""

import re
from typing import NamedTuple


class Target(NamedTuple):
    x: int
    y: int


class Move(NamedTuple):
    x: int
    y: int
    price_in_tokens: int


def compute_moves(a: Move, b: Move, target: Target) -> int | None:
    b_clicks = (target.y * a.x - target.x * a.y) / (a.x * b.y - a.y * b.x)
    a_clicks = (target.x - b.x * b_clicks) / a.x

    if a_clicks.is_integer() and b_clicks.is_integer():
        return int(a_clicks * a.price_in_tokens + b_clicks * b.price_in_tokens)
    return None


def _pp_compute(a, b, target):
    return compute_moves(a=Move(*a, 3), b=Move(*b, 1), target=Target(*target))


assert _pp_compute(a=(94, 34), b=(22, 67), target=(8400, 5400)) == 280
assert _pp_compute(a=(26, 66), b=(67, 21), target=(12748, 12176)) is None
assert _pp_compute(a=(17, 86), b=(84, 37), target=(7870, 6450)) == 200
assert _pp_compute(a=(69, 23), b=(27, 71), target=(18641, 10279)) is None


def _parse_moves_block(block: str, price: int) -> Move:
    raw_x, raw_y = re.search(r"X\+(\d+), Y\+(\d+)$", block).groups()
    return Move(int(raw_x), int(raw_y), price)


def _parse_prize_block(block: str) -> Target:
    raw_x, raw_y = re.search(r"X=(\d+), Y=(\d+)$", block).groups()
    return Target(int(raw_x) + 10000000000000, int(raw_y) + 10000000000000)


with open("2024/13_claw_contraption/input.txt") as f:
    all_tokens = 0
    splitted_by_block = f.read().split("\n\n")

    for block in splitted_by_block:
        button_a, button_b, prize = block.splitlines()
        button_a_moves = _parse_moves_block(button_a, price=3)
        button_b_moves = _parse_moves_block(button_b, price=1)
        prize_target = _parse_prize_block(prize)

        tokens = compute_moves(button_a_moves, button_b_moves, prize_target)
        all_tokens += tokens or 0

    print(all_tokens)
