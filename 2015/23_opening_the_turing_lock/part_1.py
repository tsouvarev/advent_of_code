"""
Little Jane Marie just got her very first computer for Christmas
from some unknown benefactor. It comes with instructions and an example program,
but the computer itself seems to be malfunctioning.
She's curious what the program does, and would like you to help her run it.

The manual explains that the computer supports two registers and six instructions
(truly, it goes on to remind the reader, a state-of-the-art technology).
The registers are named a and b, can hold any non-negative integer,
and begin with a value of 0. The instructions are as follows:

-   hlf r sets register r to half its current value,
    then continues with the next instruction.
-   tpl r sets register r to triple its current value,
    then continues with the next instruction.
-   inc r increments register r, adding 1 to it,
    then continues with the next instruction.
-   jmp offset is a jump;
    it continues with the instruction offset away relative to itself.
-   jie r, offset is like jmp,
    but only jumps if register r is even ("jump if even").
-   jio r, offset is like jmp,
    but only jumps if register r is 1 ("jump if one", not odd).

All three jump instructions work with an offset relative to that instruction.
The offset is always written with a prefix + or -
to indicate the direction of the jump (forward or backward, respectively).
For example, jmp +1 would simply continue with the next instruction,
while jmp +0 would continuously jump back to itself forever.

The program exits when it tries to run an instruction beyond the ones defined.

For example, this program sets a to 2,
because the jio instruction causes it to skip the tpl instruction:

inc a
jio a, +2
tpl a
inc a

What is the value in register b
when the program in your puzzle input is finished executing?
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
    registers = {"a": 0, "b": 0}

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
assert run(program) == {"a": 2, "b": 0}


with open("2015/23_opening_the_turing_lock/input.txt") as f:
    program = []
    for line in f:
        op = line[:3]
        args = line[4:].strip().split(", ")
        program.append(Instruction(Op(op), args))

    print(run(program))
