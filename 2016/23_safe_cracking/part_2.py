"""
The safe doesn't open, but it does make several angry noises to express its frustration.

You're quite sure your logic is working correctly,
so the only other thing is... you check the painting again.
As it turns out, colored eggs are still eggs. Now you count 12.

As you run the program with this new input, the prototype computer begins to overheat.
You wonder what's taking so long, and whether the lack of any instruction more powerful
than "add one" has anything to do with it. Don't bunnies usually multiply?

Anyway, what value should actually be sent to the safe?
"""

from dataclasses import dataclass
from enum import StrEnum, auto
from re import fullmatch
from typing import ClassVar, Literal, NotRequired, Protocol, TypedDict, Unpack

Register = Literal["a", "b", "c", "d"]
type Value = str
type Offset = int
type CommandReturn = tuple[Registers, list[Command], Offset]


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


class Patch(Protocol):
    pattern: ClassVar[list[Command]]

    def apply(self, registers: Registers) -> Registers: ...


class ABCyclePatch(Patch):
    pattern: ClassVar = [
        Command(Op.CPY, args=["a", "d"]),
        Command(Op.CPY, args=["0", "a"]),
        Command(Op.CPY, args=["b", "c"]),
        Command(Op.INC, args=["a"]),
        Command(Op.DEC, args=["c"]),
        Command(Op.JNZ, args=["c", "-2"]),
        Command(Op.DEC, args=["d"]),
        Command(Op.JNZ, args=["d", "-5"]),
    ]

    @classmethod
    def apply(cls, registers):
        registers["a"] = registers["a"] * registers["b"]
        return registers | {"c": 0, "d": 0}


class CDCyclePatch(Patch):
    pattern: ClassVar = [
        Command(Op.CPY, args=["94", "c"]),
        Command(Op.CPY, args=["82", "d"]),
        Command(Op.INC, args=["a"]),
        Command(Op.DEC, args=["d"]),
        Command(Op.JNZ, args=["d", "-2"]),
        Command(Op.DEC, args=["c"]),
        Command(Op.JNZ, args=["c", "-5"]),
    ]

    @classmethod
    def apply(cls, registers):
        return registers | {"a": 94 * 82, "c": 0, "d": 0}


def run(raw_commands: list[str], **registers: Unpack[Registers]) -> Registers:
    registers = dict.fromkeys("abcd", 0) | registers
    instruction_pointer = 0
    commands = [_parse_command(c) for c in raw_commands]

    handlers = {
        "cpy": _cpy,
        "inc": _inc,
        "dec": _dec,
        "jnz": _jnz,
        "tgl": _tgl,
    }

    while instruction_pointer < len(commands):
        registers, commands, offset = _optimize_loops(
            registers,
            commands,
            instruction_pointer,
        )

        if not offset:
            command = commands[instruction_pointer]
            handler = handlers[command.op]
            registers, commands, offset = handler(
                registers,
                commands,
                instruction_pointer,
                *command.args,  # type: ignore[invalid-argument-type]
            )

        instruction_pointer += offset or 1

    return registers


def _optimize_loops(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
) -> CommandReturn:
    offset = 0

    for patch in [ABCyclePatch, CDCyclePatch]:
        start = instruction_pointer
        end = start + len(patch.pattern)

        if commands[start:end] == patch.pattern:
            registers = patch.apply(registers)
            offset = len(patch.pattern)

    return registers, commands, offset


def _cpy(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    from_: Register | Value,
    to_: Register | Value,
) -> CommandReturn:
    match to_:
        case "a" | "b" | "c" | "d":
            pass
        case _:
            return registers, commands, 0

    match from_:
        case "a" | "b" | "c" | "d":
            registers[to_] = registers[from_]  # type: ignore[invalid-key]
        case str():
            registers[to_] = int(from_)  # type: ignore[invalid-key]
        case _:
            pass

    return registers, commands, 0


def _inc(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    from_: Register,
) -> CommandReturn:
    registers[from_] += 1
    return registers, commands, 0


def _dec(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    from_: Register,
) -> CommandReturn:
    registers[from_] -= 1
    return registers, commands, 0


def _jnz(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    from_: Register | Value,
    n: Value,
) -> CommandReturn:
    match from_:
        case "a" | "b" | "c" | "d":
            should_jump = bool(registers[from_])  # type: ignore[invalid-key]
        case str():
            should_jump = bool(int(from_))
        case _:
            return registers, commands, 0

    match n:
        case str() if fullmatch(r"[+-]?\d+", n):
            pass
        case "a" | "b" | "c" | "d":
            n = registers[n]  # type: ignore[invalid-key]
        case _:
            return registers, commands, 0

    return registers, commands, int(n) if should_jump else 0


def _tgl(
    registers: Registers,
    commands: list[Command],
    instruction_pointer: int,
    offset: Register | Value,
) -> CommandReturn:
    match offset:
        case "a" | "b" | "c" | "d":
            toggle_pointer = instruction_pointer + registers[offset]  # type: ignore[invalid-key]
        case _:
            raise ValueError

    if toggle_pointer >= len(commands):
        return registers, commands, 0

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
    return registers, commands, 0


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
    print(run(lines, a=12))
