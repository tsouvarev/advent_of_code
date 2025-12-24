"""
You receive a signal directly from the CPU.
Because of your recent assistance with jump instructions,
it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts:
the register to modify, whether to increase or decrease that register's value,
the amount by which to increase or decrease it, and a condition.
If the condition fails, skip the instruction without modifying the register.
The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10

These instructions would be processed as follows:

- Because a starts at 0, it is not greater than 1, and so b is not modified.
- a is increased by 1 (to 1) because b is less than 5 (it is 0).
- c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
- c is increased by -20 (to -10) because c is equal to 10.

After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to).
However, the CPU doesn't have the bandwidth
to tell you what all the registers are named,
and leaves that to you to determine.

What is the largest value in any register
after completing the instructions in your puzzle input?

To be safe, the CPU also needs to know the highest value
held in any register during this process
so that it can decide how much memory to allocate to these operations.
For example, in the above instructions,
the highest value ever held was 10
(in register c after the third instruction was evaluated).
"""

from collections import defaultdict
from enum import StrEnum, auto
from operator import eq, ge, gt, le, lt, ne
from typing import NamedTuple

type Registers = dict[Register, Value]
type Register = str
type Value = int
type Arg = str


class Condition(StrEnum):
    EQ = "=="
    NEQ = "!="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="


class Op(StrEnum):
    INC = auto()
    DEC = auto()


class Command(NamedTuple):
    register: Register
    op: Op
    value: Value
    condition: Condition
    args: tuple[Register, Value]

    def check(self, registers):
        register, value = self.args
        register_value = registers[register]

        match self.condition:
            case Condition.EQ:
                cond = eq
            case Condition.NEQ:
                cond = ne
            case Condition.LT:
                cond = lt
            case Condition.GT:
                cond = gt
            case Condition.LTE:
                cond = le
            case Condition.GTE:
                cond = ge

        return cond(register_value, value)

    def run(self, registers):
        match self.op:
            case Op.INC:
                registers[self.register] += self.value
            case Op.DEC:
                registers[self.register] -= self.value
        return registers


def run(raw_commands: list[str]) -> tuple[Registers, Value]:
    registers = defaultdict(int)
    max_value = 0

    for raw_command in raw_commands:
        command = _parse_command(raw_command)

        if command.check(registers):
            registers = command.run(registers)
            max_value = max(max_value, *registers.values())

    return registers, max_value


def _parse_command(raw_command: str) -> Command:
    register, op, value, _, arg1, condition, arg2 = raw_command.split()
    return Command(
        register, Op(op), int(value), Condition(condition), (arg1, int(arg2))
    )


command = Command("b", Op.INC, 5, Condition.GT, ("a", 1))
assert _parse_command("b inc 5 if a > 1") == command

assert command.check(defaultdict(int)) is False
assert command.check({"a": 2}) is True

assert command.run(defaultdict(int)) == {"b": 5}
assert command.run({"b": 1}) == {"b": 6}

commands = [
    "b inc 5 if a > 1",
    "a inc 1 if b < 5",
    "c dec -10 if a >= 1",
    "c inc -20 if c == 10",
]
assert run(commands) == ({"a": 1, "b": 0, "c": -10}, 10)


with open("2017/08_i_heard_you_like_registers/input.txt") as f:
    lines = [line.strip() for line in f]
    registers, max_value = run(lines)
    print(max(registers.values()), max_value)
