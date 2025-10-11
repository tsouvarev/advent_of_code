"""
You come upon a factory in which many robots are zooming around
handing small microchips to each other.

Upon closer examination, you notice that each bot only proceeds
when it has two microchips, and once it does,
it gives each one to a different bot or puts it in a marked "output" bin.
Sometimes, bots take microchips from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a single number;
the bots must use some logic to decide what to do with each chip.
You access the local control computer and download the bots' instructions
(your puzzle input).

Some of the instructions specify that a specific-valued microchip should be given
to a specific bot; the rest of the instructions indicate what a given bot
should do with its lower-value or higher-value chip.

For example, consider the following instructions:

- value 5 goes to bot 2
- bot 2 gives low to bot 1 and high to bot 0
- value 3 goes to bot 1
- bot 1 gives low to output 1 and high to bot 0
- bot 0 gives low to output 2 and high to output 0
- value 2 goes to bot 2

Initially, bot 1 starts with a value-3 chip,
and bot 2 starts with a value-2 chip and a value-5 chip.
Because bot 2 has two microchips,
it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
Then, bot 1 has two microchips;
it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.

In the end, output bin 0 contains a value-5 microchip,
output bin 1 contains a value-2 microchip,
and output bin 2 contains a value-3 microchip.
In this configuration, bot number 2 is responsible
for comparing value-5 microchips with value-2 microchips.

Based on your instructions, what is the number of the bot
that is responsible for comparing value-61 microchips with value-17 microchips?

What do you get if you multiply together
the values of one chip in each of outputs 0, 1, and 2?
"""

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import NamedTuple

from parse import parse

type State = dict[Bot | Output, list[int]]
type Rules = dict[Bot, Rule]
type Spec = Bot | Output


@dataclass(unsafe_hash=True)
class Bot:
    n: int

    @property
    def is_bot(self):
        return True


@dataclass(unsafe_hash=True)
class Output:
    n: int

    @property
    def is_bot(self):
        return False


class Rule(NamedTuple):
    low: Spec
    high: Spec


def simulate(state: State, rules: Rules) -> State:
    queue = deque()

    for who, values in state.items():
        if len(values) == 2:
            queue.append(who)

    while queue:
        bot = queue.popleft()

        for dest, value in zip(rules[bot], sorted(state[bot])):
            state[dest].append(value)
            if dest.is_bot and len(state[dest]) == 2:
                queue.append(dest)

    return state


def _parse_rules(raw_rules: list[str]) -> tuple[State, Rules]:
    state, rules = defaultdict(list), {}

    for rule in raw_rules:
        if rule.startswith("bot"):
            rules |= _parse_rule(rule)
        elif rule.startswith("value"):
            new_bots = _parse_state(rule)
            for who, val in new_bots.items():
                state[who].extend(val)
        else:
            raise ValueError(rule)

    return state, rules


def _parse_state(state: str) -> State:
    value, n = parse("value {:d} goes to bot {:d}", state).fixed
    return {Bot(n): [value]}


def _parse_rule(rule: str) -> Rules:
    spec = "bot {:d} gives low to {} and high to {}"
    n, low, high = parse(spec, rule).fixed
    bot, low, high = Bot(n), _parse_spec(low), _parse_spec(high)

    return {bot: Rule(low, high)}


def _parse_spec(spec: str) -> Bot | Output:
    if res := parse("bot {n:d}", spec):
        return Bot(res.named["n"])
    if res := parse("output {n:d}", spec):
        return Output(res.named["n"])

    raise ValueError(spec)


assert _parse_state("value 5 goes to bot 2") == {Bot(2): [5]}

rule = "bot 1 gives low to output 1 and high to bot 0"
assert _parse_rule(rule) == {Bot(1): Rule(Output(1), Bot(0))}

rules = [
    "value 5 goes to bot 2",
    "bot 2 gives low to bot 1 and high to bot 0",
    "value 3 goes to bot 1",
    "bot 1 gives low to output 1 and high to bot 0",
    "bot 0 gives low to output 2 and high to output 0",
    "value 2 goes to bot 2",
]
assert _parse_rules(rules) == (
    {
        Bot(1): [3],
        Bot(2): [5, 2],
    },
    {
        Bot(0): Rule(Output(2), Output(0)),
        Bot(1): Rule(Output(1), Bot(0)),
        Bot(2): Rule(Bot(1), Bot(0)),
    },
)

assert simulate(*_parse_rules(rules)) == {
    Bot(0): [5, 3],
    Bot(1): [3, 2],
    Bot(2): [5, 2],
    Output(0): [5],
    Output(1): [2],
    Output(2): [3],
}


with open("2016/10_balance_bots/input.txt") as f:
    state, rules = _parse_rules(f.read().splitlines())
    state = simulate(state, rules)

    for dest, values in state.items():
        if set(values) == {61, 17}:
            print(dest.n)

    print(state[Output(0)][0] * state[Output(1)][0] * state[Output(2)][0])
