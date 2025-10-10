"""
The Historians push the button on their strange device,
but this time, you all just feel like you're falling.

"Situation critical", the device announces in a familiar voice.
"Bootstrapping process failed. Initializing debugger...."

The small handheld device suddenly unfolds into an entire computer!
The Historians look around nervously before one of them tosses it to you.

This seems to be a 3-bit computer:
its program is a list of 3-bit numbers (0 through 7), like 0,1,2,3.
The computer also has three registers named A, B, and C,
but these registers aren't limited to 3 bits and can instead hold any integer.

The computer knows eight instructions,
each identified by a 3-bit number (called the instruction's opcode).
Each instruction also reads the 3-bit number after it as an input;
this is called its operand.

A number called the instruction pointer
identifies the position in the program from which the next opcode will be read;
it starts at 0, pointing at the first 3-bit number in the program.
Except for jump instructions,
the instruction pointer increases by 2 after each instruction is processed
(to move past the instruction's opcode and its operand).
If the computer tries to read an opcode past the end of the program, it instead halts.

So, the program 0,1,2,3 would run the instruction
whose opcode is 0 and pass it the operand 1,
then run the instruction having opcode 2 and pass it the operand 3, then halt.

There are two types of operands; each instruction specifies the type of its operand.
The value of a literal operand is the operand itself.
For example, the value of the literal operand 7 is the number 7.

The value of a combo operand can be found as follows:
- Combo operands 0 through 3 represent literal values 0 through 3.
- Combo operand 4 represents the value of register A.
- Combo operand 5 represents the value of register B.
- Combo operand 6 represents the value of register C.
- Combo operand 7 is reserved and will not appear in valid programs.

The eight instructions are as follows:
-   The adv instruction (opcode 0) performs division.
    The numerator is the value in the A register.
    The denominator is found
    by raising 2 to the power of the instruction's combo operand.
    (So, an operand of 2 would divide A by 4 (2^2);
    an operand of 5 would divide A by 2^B.)
    The result of the division operation is truncated to an integer
    and then written to the A register.
-   The bxl instruction (opcode 1) calculates the bitwise XOR
    of register B and the instruction's literal operand,
    then stores the result in register B.
-   The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
    (thereby keeping only its lowest 3 bits), then writes that value to the B register.
-   The jnz instruction (opcode 3) does nothing if the A register is 0.
    However, if the A register is not zero,
    it jumps by setting the instruction pointer to the value of its literal operand;
    if this instruction jumps, the instruction pointer is not increased by 2
    after this instruction.
-   The bxc instruction (opcode 4) calculates the bitwise XOR
    of register B and register C, then stores the result in register B.
    (For legacy reasons, this instruction reads an operand but ignores it.)
-   The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
    then outputs that value.
    (If a program outputs multiple values, they are separated by commas.)
-   The bdv instruction (opcode 6) works exactly like the adv instruction
    except that the result is stored in the B register.
    (The numerator is still read from the A register.)
-   The cdv instruction (opcode 7) works exactly like the adv instruction
    except that the result is stored in the C register.
    (The numerator is still read from the A register.)

Here are some examples of instruction operation:
-   If register C contains 9, the program 2,6 would set register B to 1.
-   If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
-   If register A contains 2024, the program 0,1,5,4,3,0
    would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
-   If register B contains 29, the program 1,7 would set register B to 26.
-   If register B contains 2024 and register C contains 43690,
    the program 4,0 would set register B to 44354.

The Historians' strange device has finished initializing its debugger
and is displaying some information about the program it is trying to run
(your puzzle input). For example:

Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0

Your first task is to determine what the program is trying to output.
To do this, initialize the registers to the given values,
then run the given program, collecting any output produced by out instructions.
(Always join the values produced by out instructions with commas.)
After the above program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.

Using the information provided by the debugger,
initialize the registers to the given values, then run the program.
Once it halts, what do you get
if you use commas to join the values it output into a single string?
"""

from dataclasses import dataclass, field
from enum import IntEnum
from itertools import batched, chain
from typing import NamedTuple, TypedDict

type Program = list[int]
type LiteralOperand = int
type ComboOperand = int


class Registers(TypedDict):
    A: int
    B: int
    C: int


class Instruction(NamedTuple):
    operation: Op
    operand: int


@dataclass
class Return:
    registers: Registers
    jump: int | None = field(default=None)
    output: str = field(default="")


class Op(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

    @property
    def executor(self):
        return {
            self.ADV: _adv,
            self.BXL: _bxl,
            self.BST: _bst,
            self.JNZ: _jnz,
            self.BXC: _bxc,
            self.OUT: _out,
            self.BDV: _bdv,
            self.CDV: _cdv,
        }[self]


def compute(program: Program, registers: Registers) -> str:
    instructions = _parse_instructions(program)
    ip = 0
    output = []

    while True:
        try:
            instruction = instructions[ip]
        except IndexError:
            break

        executor = instruction.operation.executor
        returned = executor(instruction.operand, registers)

        registers |= returned.registers
        ip = returned.jump if returned.jump is not None else ip + 1

        if returned.output != "":
            output.append(returned.output)

    return ",".join(output)


def _adv(operand: ComboOperand, registers: Registers) -> Return:
    value = _get_operand_value(operand, registers)
    update = {"A": registers["A"] // 2**value}
    return Return(update)


def _bxl(value: LiteralOperand, registers: Registers) -> Return:
    update = {"B": registers["B"] ^ value}
    return Return(update)


def _bst(operand: ComboOperand, registers: Registers) -> Return:
    value = _get_operand_value(operand, registers)
    update = {"B": value % 8}
    return Return(update)


def _jnz(value: LiteralOperand, registers: Registers) -> Return:
    if registers["A"] == 0:
        return Return({})

    return Return({}, jump=value // 2)


def _bxc(operand: ComboOperand, registers: Registers) -> Return:
    _get_operand_value(operand, registers)
    update = {"B": registers["B"] ^ registers["C"]}
    return Return(update)


def _out(operand: ComboOperand, registers: Registers) -> Return:
    value = _get_operand_value(operand, registers)
    return Return({}, output=str(value % 8))


def _bdv(operand: ComboOperand, registers: Registers) -> Return:
    value = _get_operand_value(operand, registers)
    update = {"B": registers["A"] // 2**value}
    return Return(update)


def _cdv(operand: ComboOperand, registers: Registers) -> Return:
    value = _get_operand_value(operand, registers)
    update = {"C": registers["A"] // 2**value}
    return Return(update)


def _parse_instructions(program: Program) -> list[Instruction]:
    return [
        Instruction(Op(operation), operand)
        for operation, operand in batched(program, n=2)
    ]


def _get_operand_value(operand: int, registers: Registers) -> int:
    if 0 <= operand <= 3:
        return operand

    if operand == 4:
        return registers["A"]

    if operand == 5:
        return registers["B"]

    if operand == 6:
        return registers["C"]

    msg = "Bad operand"
    raise ValueError(msg)


def _to_program(*instructions: Instruction) -> list[int]:
    return list(chain.from_iterable(instructions))


assert _parse_instructions([0, 1, 2, 3]) == [(Op.ADV, 1), (Op.BST, 3)]
assert _parse_instructions([0, 1, 5, 4, 3, 0]) == [
    (Op.ADV, 1),
    (Op.OUT, 4),
    (Op.JNZ, 0),
]

assert _adv(1, {"A": 4}) == Return({"A": 2})
assert _adv(1, {"A": 5}) == Return({"A": 2})

assert _bxl(1, {"B": 2}) == Return({"B": 3})
assert _bxl(4, {"B": 2}) == Return({"B": 6})

assert _bst(1, {}) == Return({"B": 1})
assert _bst(4, {"A": 10}) == Return({"B": 2})

assert _jnz(4, {"A": 0}) == Return({}, jump=None)
assert _jnz(4, {"A": 1}) == Return({}, jump=2)

assert _bxc(1, {"B": 1, "C": 2}) == Return({"B": 3})

assert _out(1, {}) == Return({}, output="1")
assert _out(4, {"A": 10}) == Return({}, output="2")

assert _bdv(1, {"A": 4}) == Return({"B": 2})
assert _bdv(1, {"A": 5}) == Return({"B": 2})

assert _cdv(1, {"A": 4}) == Return({"C": 2})
assert _cdv(1, {"A": 5}) == Return({"C": 2})

assert _get_operand_value(0, {}) == 0
assert _get_operand_value(1, {}) == 1
assert _get_operand_value(2, {}) == 2
assert _get_operand_value(3, {}) == 3
assert _get_operand_value(4, {"A": 1}) == 1
assert _get_operand_value(5, {"B": 1}) == 1
assert _get_operand_value(6, {"C": 1}) == 1

i = _to_program((Op.ADV, 1), (Op.OUT, 1), (Op.JNZ, 0))
r = {"A": 4, "B": 0, "C": 0}
assert compute(i, r) == "1,1,1"

i = _to_program((Op.OUT, 1), (Op.ADV, 1), (Op.OUT, 1), (Op.JNZ, 2))
r = {"A": 4, "B": 0, "C": 0}
assert compute(i, r) == "1,1,1,1"

assert compute([0, 1, 5, 4, 3, 0], {"A": 729, "B": 0, "C": 0}) == "4,6,3,5,6,3,5,2,1,0"

print(
    compute(
        [2, 4, 1, 1, 7, 5, 1, 5, 4, 3, 0, 3, 5, 5, 3, 0],
        {"A": 46_323_429, "B": 0, "C": 0},
    ),
)
