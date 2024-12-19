"""
As you scan through the corrupted memory,
you notice that some of the conditional statements are also still intact.
If you handle some of the uncorrupted conditional statements in the program,
you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:
- The do() instruction enables future mul instructions.
- The don't() instruction disables future mul instructions.

Only the most recent do() or don't() instruction applies.
At the beginning of the program, mul instructions are enabled.

For example:
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

This corrupted memory is similar to the example from before,
but this time the mul(5,5) and mul(11,8) instructions are disabled
because there is a don't() instruction before them.
The other mul instructions function normally,
including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions;
what do you get if you add up all of the results of just the enabled multiplications?
"""

from operator import mul
import re


def fix_mul_conditional(data):
    all_muls = []
    for statement in data.split("do()"):
        s = statement.split("don't()", 1)[0]
        all_muls.extend(re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", s))

    return sum(mul(*map(int, args)) for args in all_muls)


assert fix_mul_conditional("do()mul(123,4)") == 123 * 4
assert fix_mul_conditional("don't()mul(44,46)") == 0
assert fix_mul_conditional("do()don't()mul(4,4)") == 0
assert fix_mul_conditional("mul(4,4)xmul(2,3)") == 4 * 4 + 2 * 3

long_exp = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
assert fix_mul_conditional(long_exp) == 2 * 4 + 8 * 5


with open("3_mull_it_over_input.txt") as f:
    print(fix_mul_conditional(f.read()))
