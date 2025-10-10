"""
Now, take the signal you got on wire a, override wire b to that signal,
and reset the other wires (including wire a).

What new signal is ultimately provided to wire a?
"""

from enum import StrEnum, auto
from graphlib import TopologicalSorter
from operator import and_, lshift, or_, rshift
from typing import NamedTuple


class Gate(NamedTuple):
    operation: Operation
    to_: str
    inputs: list[str]
    operands: list[str | int]


class Operation(StrEnum):
    INPUT = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    LSHIFT = auto()
    RSHIFT = auto()

    def get_executor(self):
        return {
            Operation.INPUT: lambda x: x,
            Operation.AND: and_,
            Operation.OR: or_,
            Operation.NOT: bit_invert,
            Operation.LSHIFT: lshift,
            Operation.RSHIFT: rshift,
        }[self]


def compute(inputs: list[str]) -> dict[str, int]:
    values = {}

    gates = [_parse(input_) for input_ in inputs]
    gates = {gate.to_: gate for gate in gates}
    sorted_gates = _sort_gates(gates)

    for to_, gate in sorted_gates.items():
        resolved_operands = list(_get_operands(gate, values))
        executor = gate.operation.get_executor()
        values[to_] = executor(*resolved_operands)

    return values


def _sort_gates(gates: dict[str, Gate]):
    ts = TopologicalSorter()
    for gate in gates.values():
        ts.add(gate.to_, *gate.inputs)

    return {raw_gate: gates[raw_gate] for raw_gate in ts.static_order()}


def _get_operands(gate, values):
    for operand in gate.operands:
        if isinstance(operand, int):
            yield operand
        else:
            yield values[operand]


def _parse(expr: str) -> Gate:
    stat, to_ = expr.split(" -> ")

    if "AND" in stat:
        inputs = stat.split(" AND ")
        return Gate(Operation.AND, to_, *_parse_inputs_and_operands(*inputs))
    if "OR" in stat:
        inputs = stat.split(" OR ")
        return Gate(Operation.OR, to_, *_parse_inputs_and_operands(*inputs))
    if "NOT" in stat:
        input_ = stat.removeprefix("NOT ")
        return Gate(Operation.NOT, to_, [input_], [input_])
    if "LSHIFT" in stat:
        input_, value = stat.split(" LSHIFT ")
        return Gate(Operation.LSHIFT, to_, [input_], [input_, int(value)])
    if "RSHIFT" in stat:
        input_, value = stat.split(" RSHIFT ")
        return Gate(Operation.RSHIFT, to_, [input_], [input_, int(value)])

    return Gate(Operation.INPUT, to_, *_parse_inputs_and_operands(stat))


def _parse_inputs_and_operands(*values: str) -> tuple[list[str], list[str | int]]:
    inputs, operands = [], []
    for value in values:
        if value.isnumeric():
            operands.append(int(value))
        else:
            inputs.append(value)
            operands.append(value)

    return inputs, operands


def bit_invert(n: int) -> int:
    return ~n & 0xFFFF


def _to_instr_dict(inputs: list[str]) -> dict[str, Gate]:
    gates = map(_parse, inputs)
    return {gate.to_: gate for gate in gates}


assert _parse("123 -> x") == Gate(Operation.INPUT, "x", [], [123])
assert _parse("a -> x") == Gate(Operation.INPUT, "x", ["a"], ["a"])
assert _parse("x AND y -> d") == Gate(Operation.AND, "d", ["x", "y"], ["x", "y"])
assert _parse("1 AND y -> d") == Gate(Operation.AND, "d", ["y"], [1, "y"])
assert _parse("y AND 1 -> d") == Gate(Operation.AND, "d", ["y"], ["y", 1])
assert _parse("x OR y -> e") == Gate(Operation.OR, "e", ["x", "y"], ["x", "y"])
assert _parse("1 OR y -> e") == Gate(Operation.OR, "e", ["y"], [1, "y"])
assert _parse("y OR 1 -> e") == Gate(Operation.OR, "e", ["y"], ["y", 1])
assert _parse("x LSHIFT 2 -> f") == Gate(Operation.LSHIFT, "f", ["x"], ["x", 2])
assert _parse("y RSHIFT 2 -> g") == Gate(Operation.RSHIFT, "g", ["y"], ["y", 2])
assert _parse("NOT x -> h") == Gate(Operation.NOT, "h", ["x"], ["x"])

inputs = [
    "x OR y -> e",
    "x LSHIFT 2 -> f",
    "y RSHIFT 2 -> g",
    "x AND y -> d",
    "NOT x -> h",
    "NOT y -> i",
    "123 -> x",
    "456 -> y",
]
assert list(_sort_gates(_to_instr_dict(inputs))) == [
    "x",
    "y",
    "f",
    "h",
    "e",
    "g",
    "d",
    "i",
]

assert compute(["123 -> x"]) == {"x": 123}

inputs = [
    "123 -> x",
    "456 -> y",
    "x AND y -> d",
    "x OR y -> e",
    "x LSHIFT 2 -> f",
    "y RSHIFT 2 -> g",
    "NOT x -> h",
    "NOT y -> i",
]
assert compute(inputs) == {
    "x": 123,
    "y": 456,
    "f": 492,
    "h": 65412,
    "d": 72,
    "e": 507,
    "g": 114,
    "i": 65079,
}

with open("2015/07_some_assembly_required/input_2.txt") as f:
    print(compute(f.read().splitlines())["a"])
