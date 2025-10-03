"""
The unknown benefactor is very thankful for releasi--
er, helping little Jane Marie with her computer.
Definitely not to distract you, what is the value in register b
after the program is finished executing if register a starts as 1 instead?
"""

from enum import StrEnum, auto
from typing import NamedTuple


class Op(StrEnum):
    HLF = auto()
    TPL = auto()
    INC = auto()
    JMP = auto()
    JIE = auto()
    JIO = auto()

    def get_runner(self):
        return {
            Op.HLF: hlf,
            Op.TPL: tpl,
            Op.INC: inc,
            Op.JMP: jmp,
            Op.JIE: jie,
            Op.JIO: jio,
        }[self]


class Instruction(NamedTuple):
    op: Op
    args: list[str]


def hlf(registers: dict, r: str) -> dict:
    registers[r] = registers[r] / 2
    return registers, None


def tpl(registers: dict, r: str) -> dict:
    registers[r] = registers[r] * 3
    return registers, None


def inc(registers: dict, r: str) -> dict:
    registers[r] = registers[r] + 1
    return registers, None


def jmp(registers: dict, r: str) -> dict:
    return registers, int(r)


def jie(registers: dict, r: str, offset: str) -> dict:
    return registers, int(offset) if registers[r] % 2 == 0 else None


def jio(registers: dict, r: str, offset: str) -> dict:
    return registers, int(offset) if registers[r] == 1 else None


def run(instructions: list[Instruction]) -> dict:
    pointer = 0
    registers = {"a": 1, "b": 0}

    while pointer < len(instructions):
        instruction = instructions[pointer]
        registers, offset = instruction.op.get_runner()(registers, *instruction.args)

        pointer += offset if offset is not None else 1

    return registers


assert hlf({"a": 2}, "a") == ({"a": 1}, None)
assert tpl({"a": 1}, "a") == ({"a": 3}, None)
assert inc({"a": 1}, "a") == ({"a": 2}, None)
assert jmp({"a": 1}, "1") == ({"a": 1}, 1)
assert jie({"a": 1}, "a", "-1") == ({"a": 1}, None)
assert jie({"a": 2}, "a", "-1") == ({"a": 2}, -1)
assert jio({"a": 1}, "a", "-1") == ({"a": 1}, -1)
assert jio({"a": 2}, "a", "-1") == ({"a": 2}, None)

program = [
    Instruction(Op.INC, ["a"]),
    Instruction(Op.JIO, ["a", "+2"]),
    Instruction(Op.TPL, ["a"]),
    Instruction(Op.INC, ["a"]),
]
assert run(program) == {"a": 7, "b": 0}


with open("2015/23_opening_the_turing_lock/input.txt") as f:
    program = []
    for line in f:
        op = line[:3]
        args = line[4:].strip().split(", ")
        program.append(Instruction(Op(op), args))

    print(run(program))
