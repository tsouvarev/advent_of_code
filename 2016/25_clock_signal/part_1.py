"""
You open the door and find yourself on the roof.
The city sprawls away from you for miles and miles.

There's not much time now - it's already Christmas,
but you're nowhere near the North Pole,
much too far to deliver these stars to the sleigh in time.

However, maybe the huge antenna up here can offer a solution.
After all, the sleigh doesn't need the stars, exactly;
it needs the timing data they provide,
and you happen to have a massive signal generator right here.

You connect the stars you have to your prototype computer,
connect that to the antenna, and begin the transmission.

Nothing happens.

You call the service number printed on the side of the antenna
and quickly explain the situation.
"I'm not sure what kind of equipment you have connected over there," he says,
"but you need a clock signal." You try to explain that this is a signal for a clock.

"No, no, a clock signal - timing information
so the antenna computer knows how to read the data you're sending it.
An endless, alternating pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.

You ask if the antenna can handle a clock signal
at the frequency you would need to use for the data from the stars.
"There's no way it can! The only antenna we've installed capable of that
is on top of a top-secret Easter Bunny installation,
and you're definitely not-" You hang up the phone.

You've extracted the antenna's clock signal generation assembunny code
(your puzzle input); it looks mostly compatible with code you worked on just recently.

This antenna code, being a signal generator, uses one extra instruction:

-   `out x` transmits x (either an integer or the value of a register)
    as the next value for the clock signal.

The code takes a value (via register a) that describes the signal to generate,
but you're not sure how it's used.
You'll have to find the input to produce the right signal through experimentation.

What is the lowest positive integer that can be used to initialize register a
and cause the code to output a clock signal of 0, 1, 0, 1... repeating forever?
"""

from itertools import count
from typing import Literal, NamedTuple, NotRequired, TypedDict, Unpack

Register = Literal["a", "b", "c", "d"]
type Value = str
type Offset = int
type Output = str


class Return(NamedTuple):
    registers: Registers
    offset: Offset
    output: Output


class Registers(TypedDict):
    a: NotRequired[int]
    b: NotRequired[int]
    c: NotRequired[int]
    d: NotRequired[int]


def run(
    commands: list[str],
    required_output: str,
    **registers: Unpack[Registers],
) -> Registers:
    registers = dict.fromkeys("abcd", 0) | registers
    instruction_pointer, offset = 0, 0
    all_output = ""

    handlers = {
        "cpy": _cpy,
        "inc": _inc,
        "dec": _dec,
        "jnz": _jnz,
        "out": _out,
    }
    res = Return(registers, offset, "")

    while instruction_pointer < len(commands):
        raw_command = commands[instruction_pointer]
        op, *args = raw_command.split(" ")

        handler = handlers[op]
        res = handler(res.registers, *args)  # type: ignore[invalid-argument-type]

        if res.output:
            all_output += res.output
            if len(all_output) > len(required_output):
                return res.registers
            if not required_output.startswith(all_output):
                raise ValueError(all_output)

        instruction_pointer += res.offset or 1

    return res.registers


def _cpy(registers: Registers, from_: Register | Value, to_: Register) -> Return:
    match from_:
        case "a" | "b" | "c" | "d":
            registers[to_] = registers[from_]  # type: ignore[invalid-key]
        case str():
            registers[to_] = int(from_)
        case _:
            raise ValueError(from_)

    return Return(registers, 0, "")


def _inc(registers: Registers, from_: Register) -> Return:
    registers[from_] += 1
    return Return(registers, 0, "")


def _dec(registers: Registers, from_: Register) -> Return:
    registers[from_] -= 1
    return Return(registers, 0, "")


def _jnz(registers: Registers, from_: Register | Value, n: Value) -> Return:
    match from_:
        case "a" | "b" | "c" | "d":
            should_jump = bool(registers[from_])  # type: ignore[invalid-key]
        case str():
            should_jump = bool(int(from_))
        case _:
            raise ValueError(from_)

    return Return(registers, int(n) if should_jump else 0, "")


def _out(registers: Registers, x: Register | Value) -> Return:
    match x:
        case "a" | "b" | "c" | "d":
            x = registers[x]  # type: ignore[invalid-key]
        case str():
            pass

    return Return(registers, 0, str(x))


assert _cpy({"a": 0}, "42", "a") == ({"a": 42}, 0, "")
assert _cpy({"a": 0, "b": 1}, "b", "a") == ({"a": 1, "b": 1}, 0, "")

assert _inc({"a": 0}, "a") == ({"a": 1}, 0, "")

assert _dec({"a": 1}, "a") == ({"a": 0}, 0, "")

assert _jnz({"a": 0}, "a", "2") == ({"a": 0}, 0, "")
assert _jnz({"a": 1}, "a", "2") == ({"a": 1}, 2, "")
assert _jnz({"a": 0}, "0", "2") == ({"a": 0}, 0, "")
assert _jnz({"a": 1}, "1", "2") == ({"a": 1}, 2, "")

commands = ["cpy 41 a", "inc a", "inc a", "dec a", "jnz a 2", "dec a"]
assert run(commands, "") == {"a": 42, "b": 0, "c": 0, "d": 0}


with open("2016/25_clock_signal/input.txt") as f:
    lines = [line.strip() for line in f]

    for a in count(1):
        output = "01" * 1000
        try:
            run(lines, required_output=output, a=a)
        except ValueError as e:
            print(f"{a}:\t{e}")
        else:
            print(a)
            break
