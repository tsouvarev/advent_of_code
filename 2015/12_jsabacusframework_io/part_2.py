"""
Uh oh - the Accounting-Elves have realized that they double-counted everything red.

Ignore any object (and all of its children) which has any property with the value "red".
Do this only for objects ({...}), not arrays ([...]).
-   [1,2,3] still has a sum of 6.
-   [1,{"c":"red","b":2},3] now has a sum of 4, because the middle object is ignored.
-   {"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0,
    because the entire structure is ignored.
-   [1,"red",5] has a sum of 6, because "red" in an array has no effect.
"""

from json import loads


def sum_numbers(document: list | dict | str | int) -> int:
    match document:
        case list():
            return sum(sum_numbers(el) for el in document)
        case dict():
            return (
                sum(sum_numbers(el) for el in document.values())
                if "red" not in document.values()
                else 0
            )
        case str():
            return 0
        case int():
            return document


assert sum_numbers(loads("[1,2,3]")) == 6
assert sum_numbers(loads('{"a":2,"b":4}')) == 6
assert sum_numbers(loads("[[[3]]]")) == 3
assert sum_numbers(loads('{"a":{"b":4},"c":-1}')) == 3
assert sum_numbers(loads('{"a":[-1,1]}')) == 0
assert sum_numbers(loads('[-1,{"a":1}]')) == 0
assert sum_numbers(loads("[]")) == 0
assert sum_numbers(loads("{}")) == 0

assert sum_numbers(loads('[1,{"c":"red","b":2},3]')) == 4
assert sum_numbers(loads('{"d":"red","e":[1,2,3,4],"f":5}')) == 0
assert sum_numbers(loads('[1,"red",5]')) == 6


with open("2015/12_jsabacusframework_io/input.txt") as f:
    print(sum_numbers(loads(f.read())))
