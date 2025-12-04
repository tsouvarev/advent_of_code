"""
This is one of the top floors of the nicest tower in EBHQ.
The Easter Bunny's private office is here,
complete with a safe hidden behind a painting,
and who wouldn't hide a star in a safe behind a painting?

The safe has a digital screen and keypad for code entry.
A sticky note attached to the safe has a password hint on it: "eggs".
The painting is of a large rabbit coloring some eggs. You see 7.

When you go to type the code, though, nothing appears on the display;
instead, the keypad comes apart in your hands, apparently having been smashed.
Behind it is some kind of socket -
one that matches a connector in your prototype computer!
You pull apart the smashed keypad and extract the logic circuit,
plug it into your computer, and plug your computer into the safe.

Now, you just need to figure out what output the keypad would have sent to the safe.
You extract the assembunny code from the logic chip (your puzzle input).

The code looks like it uses almost the same architecture
and instruction set that the monorail computer used!
You should be able to use the same assembunny interpreter
for this as you did there, but with one new instruction:

`tgl x` toggles the instruction x away
(pointing at instructions like jnz does:
 positive means forward; negative means backward):

-   For one-argument instructions,
    inc becomes dec, and all other one-argument instructions become inc.
-   For two-argument instructions,
    jnz becomes cpy, and all other two-instructions become jnz.
-   The arguments of a toggled instruction are not affected.
-   If an attempt is made to toggle an instruction outside the program,
    nothing happens.
-   If toggling produces an invalid instruction (like cpy 1 2)
    and an attempt is later made to execute that instruction, skip it instead.
-   If tgl toggles itself
    (for example, if a is 0, tgl a would target itself and become inc a),
    the resulting instruction is not executed until the next time it is reached.

For example, given this program:

cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a

-   cpy 2 a initializes register a to 2.
-   The first tgl a toggles an instruction a (2) away from it,
    which changes the third tgl a into inc a.
-   The second tgl a also modifies an instruction 2 away from it,
    which changes the cpy 1 a into jnz 1 a.
-   The fourth line, which is now inc a, increments a to 3.
-   Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions ahead,
    skipping the dec a instructions.

In this example, the final value in register a is 3.

The rest of the electronics
seem to place the keypad entry (the number of eggs, 7) in register a, run the code,
and then send the value left in register a to the safe.

What value should be sent to the safe?
"""

from dataclasses import dataclass
from enum import StrEnum, auto
from re import fullmatch
from typing import Literal, NamedTuple, NotRequired, TypedDict, Unpack

Register = Literal["a", "b", "c", "d"]
type Value = str
type Offset = int


class Return(NamedTuple):
    registers: Registers
    commands: list[Command]
    offset: Offset


@dataclass
class Command:
    op: Op
    args: list[str]


class Op(StrEnum):
    INC = auto()
    DEC = auto()
    TGL = auto()
    CPY = auto()
    JNZ = auto()


class Registers(TypedDict):
    a: NotRequired[int]
    b: NotRequired[int]
    c: NotRequired[int]
    d: NotRequired[int]


def run(raw_commands: list[str], **registers: Unpack[Registers]) -> Registers:
    registers = dict.fromkeys("abcd", 0) | registers
    instruction_pointer, offset = 0, 0
    commands = [_parse_command(c) for c in raw_commands]

    handlers = {
        "cpy": _cpy,
        "inc": _inc,
        "dec": _dec,
        "jnz": _jnz,
        "tgl": _tgl,
    }
    res = Return(registers, commands, offset)

    while instruction_pointer < len(res.commands):
        command = res.commands[instruction_pointer]
        handler = handlers[command.op]
        res = handler(
            res.registers,
            res.commands,
            instruction_pointer,
            *command.args,  # type: ignore[invalid-argument-type]
        )
        instruction_pointer += res.offset or 1

    return res.registers


def _cpy(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    from_: Register | Value,
    to_: Register,
) -> Return:
    match to_:
        case "a" | "b" | "c" | "d":
            pass
        case _:
            return Return(registers, commands, 0)

    match from_:
        case "a" | "b" | "c" | "d":
            registers[to_] = registers[from_]  # type: ignore[invalid-key]
        case str():
            registers[to_] = int(from_)
        case _:
            pass

    return Return(registers, commands, 0)


def _inc(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    from_: Register,
) -> Return:
    registers[from_] += 1
    return Return(registers, commands, 0)


def _dec(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    from_: Register,
) -> Return:
    registers[from_] -= 1
    return Return(registers, commands, 0)


def _jnz(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    from_: Register | Value,
    n: Value,
) -> Return:
    match from_:
        case "a" | "b" | "c" | "d":
            should_jump = bool(registers[from_])  # type: ignore[invalid-key]
        case str():
            should_jump = bool(int(from_))
        case _:
            return Return(registers, commands, 0)

    match n:
        case str() if fullmatch(r"[+-]?\d+", n):
            pass
        case "a" | "b" | "c" | "d":
            n = registers[n]  # type: ignore[invalid-key]
        case _:
            return Return(registers, commands, 0)

    return Return(registers, commands, int(n) if should_jump else 0)


def _tgl(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    offset: Register | Value,
) -> Return:
    match offset:
        case "a" | "b" | "c" | "d":
            toggle_pointer = instruction_pointer + registers[offset]  # type: ignore[invalid-key]
        case _:
            raise ValueError

    if toggle_pointer >= len(commands):
        return Return(registers, commands, 0)

    command_to_change = commands[toggle_pointer]
    match command_to_change.op:
        case Op.INC:
            new_op = Op.DEC
        case Op.DEC:
            new_op = Op.INC
        case Op.TGL:
            new_op = Op.INC
        case Op.JNZ:
            new_op = Op.CPY
        case Op.CPY:
            new_op = Op.JNZ

    command_to_change.op = new_op
    return Return(registers, commands, 0)


def _parse_command(raw_command: str) -> Command:
    op, *args = raw_command.split(" ")
    return Command(Op(op), args)


assert _cpy({"a": 0}, [], 0, "42", "a") == ({"a": 42}, [], 0)
assert _cpy({"a": 0, "b": 1}, [], 0, "b", "a") == ({"a": 1, "b": 1}, [], 0)

assert _inc({"a": 0}, [], 0, "a") == ({"a": 1}, [], 0)

assert _dec({"a": 1}, [], 0, "a") == ({"a": 0}, [], 0)

assert _jnz({"a": 0}, [], 0, "a", "2") == ({"a": 0}, [], 0)
assert _jnz({"a": 1}, [], 0, "a", "2") == ({"a": 1}, [], 2)
assert _jnz({"a": 0}, [], 0, "0", "2") == ({"a": 0}, [], 0)
assert _jnz({"a": 1}, [], 0, "1", "2") == ({"a": 1}, [], 2)

commands = ["cpy 41 a", "inc a", "inc a", "dec a", "jnz a 2", "dec a"]
assert run(commands) == {"a": 42, "b": 0, "c": 0, "d": 0}

commands = [
    "cpy 2 a",
    "tgl a",
    "tgl a",
    "tgl a",
    "cpy 1 a",
    "dec a",
    "dec a",
]
assert run(commands) == {"a": 3, "b": 0, "c": 0, "d": 0}


with open("2016/23_safe_cracking/input.txt") as f:
    lines = [line.strip() for line in f]
    print(run(lines, a=7))
