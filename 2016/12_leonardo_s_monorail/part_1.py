"""
You finally reach the top floor of this building: a garden with a slanted glass ceiling.
Looks like there are no more stars to be had.

While sitting on a nearby bench amidst some tiger lilies,
you manage to decrypt some of the files you extracted from the servers downstairs.

According to these documents, Easter Bunny HQ isn't just this building -
it's a collection of buildings in the nearby area.
They're all connected by a local monorail,
and there's another building not far from here!
Unfortunately, being night, the monorail is currently not operating.

You remotely connect to the monorail control systems
and discover that the boot sequence expects a password.
The password-checking logic (your puzzle input) is easy to extract,
but the code it uses is strange:
it's assembunny code designed for the new computer you just assembled.
You'll have to execute the code and get the password.

The assembunny code you've extracted operates on four registers (a, b, c, and d)
that start at 0 and can hold any integer.
However, it seems to make use of only a few instructions:

-   cpy x y copies x (either an integer or the value of a register) into register y.
-   inc x increases the value of register x by one.
-   dec x decreases the value of register x by one.
-   jnz x y jumps to an instruction y away (positive means forward;
    negative means backward), but only if x is not zero.

The jnz instruction moves relative to itself:
an offset of -1 would continue at the previous instruction,
while an offset of 2 would skip over the next instruction.

For example:

cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a

The above code would set register a to 41, increase its value by 2,
decrease its value by 1, and then skip the last dec a
(because a is not zero, so the jnz a 2 skips it), leaving register a at 42.
When you move past the last instruction, the program halts.

After executing the assembunny code in your puzzle input,
what value is left in register a?

If you instead initialize register c to be 1, what value is now left in register a?
"""

from typing import Literal, NamedTuple, NotRequired, TypedDict, Unpack

Register = Literal["a", "b", "c", "d"]
type Value = str
type Offset = int


class Return(NamedTuple):
    registers: Registers
    offset: Offset


class Registers(TypedDict):
    a: NotRequired[int]
    b: NotRequired[int]
    c: NotRequired[int]
    d: NotRequired[int]


def run(commands: list[str], **registers: Unpack[Registers]) -> Registers:
    registers = dict.fromkeys("abcd", 0) | registers
    instruction_pointer, offset = 0, 0

    handlers = {
        "cpy": _cpy,
        "inc": _inc,
        "dec": _dec,
        "jnz": _jnz,
    }
    res = Return(registers, offset)

    while instruction_pointer < len(commands):
        raw_command = commands[instruction_pointer]
        op, *args = raw_command.split(" ")

        handler = handlers[op]
        res = handler(
            res.registers,
            *args,  # type: ignore[invalid-argument-type]
        )
        instruction_pointer += res.offset or 1

    return registers


def _cpy(registers: Registers, from_: Register | Value, to_: Register) -> Return:
    match from_:
        case "a" | "b" | "c" | "d":
            registers[to_] = registers[from_]  # type: ignore[invalid-key]
        case str():
            registers[to_] = int(from_)
        case _:
            raise ValueError(from_)

    return Return(registers, 0)


def _inc(registers: Registers, from_: Register) -> Return:
    registers[from_] += 1
    return Return(registers, 0)


def _dec(registers: Registers, from_: Register) -> Return:
    registers[from_] -= 1
    return Return(registers, 0)


def _jnz(registers: Registers, from_: Register | Value, n: Value) -> Return:
    match from_:
        case "a" | "b" | "c" | "d":
            should_jump = bool(registers[from_])  # type: ignore[invalid-key]
        case str():
            should_jump = bool(int(from_))
        case _:
            raise ValueError(from_)

    return Return(registers, int(n) if should_jump else 0)


assert _cpy({"a": 0}, "42", "a") == ({"a": 42}, 0)
assert _cpy({"a": 0, "b": 1}, "b", "a") == ({"a": 1, "b": 1}, 0)

assert _inc({"a": 0}, "a") == ({"a": 1}, 0)

assert _dec({"a": 1}, "a") == ({"a": 0}, 0)

assert _jnz({"a": 0}, "a", "2") == ({"a": 0}, 0)
assert _jnz({"a": 1}, "a", "2") == ({"a": 1}, 2)
assert _jnz({"a": 0}, "0", "2") == ({"a": 0}, 0)
assert _jnz({"a": 1}, "1", "2") == ({"a": 1}, 2)

commands = ["cpy 41 a", "inc a", "inc a", "dec a", "jnz a 2", "dec a"]
assert run(commands) == {"a": 42, "b": 0, "c": 0, "d": 0}


with open("2016/12_leonardo_s_monorail/input.txt") as f:
    commands = list(f.read().splitlines())
    print(run(commands))
    print(run(commands, c=1))
