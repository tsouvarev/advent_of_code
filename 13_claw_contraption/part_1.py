"""
Next up: the lobby of a resort on a tropical island.
The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade!
Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual.
Instead of a joystick or directional buttons to control the claw,
these machines have two buttons labeled A and B.
Worse, you can't just put in a token and play;
it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured
to move the claw a specific amount to the right (along the X axis)
and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned
exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend
to win as many prizes as possible? You assemble a list
of every machine's button behavior and prize location (your puzzle input).
For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279

This list describes the button configuration
and prize location of four different claw machines.

For now, consider just the first claw machine in the list:
-   Pushing the machine's A button would move the claw
    94 units along the X axis and 34 units along the Y axis.
-   Pushing the B button would move the
    claw 22 units along the X axis and 67 units along the Y axis.
-   The prize is located at X=8400, Y=5400;
    this means that from the claw's initial position, it would need to move exactly
    8400 units along the X axis and exactly 5400 units along the Y axis
    to be perfectly aligned with the prize in this machine.

The cheapest way to win the prize is
by pushing the A button 80 times and the B button 40 times.
This would line up the claw along the X axis (because 80*94 + 40*22 = 8400)
and along the Y axis (because 80*34 + 40*67 = 5400).
Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses,
a total of 280 tokens.

For the second and fourth claw machines,
there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is
by pushing the A button 38 times and the B button 86 times.
Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two;
the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed
no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible.
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
    return Target(int(raw_x), int(raw_y))


with open("13_claw_contraption/input.txt") as f:
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
