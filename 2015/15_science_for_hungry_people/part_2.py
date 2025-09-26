"""
Your cookie recipe becomes wildly popular!
Someone asks if you can make another recipe that has exactly 500 calories per cookie
(so they can use it as a meal replacement).
Keep the rest of your award-winning process the same
(100 teaspoons, same ingredients, same scoring system).

For example, given the ingredients above,
if you had instead selected 40 teaspoons of butterscotch and 60 teaspoons of cinnamon
(which still adds to 100), the total calorie count would be 40*8 + 60*3 = 500.
The total score would go down, though: only 57600000,
the best you can do in such trying circumstances.

Given the ingredients in your kitchen and their properties,
what is the total score of the highest-scoring cookie
you can make with a calorie total of 500?
"""

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import product

from parse import parse


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def max_score(ingredients: list[Ingredient], volume: int, calories: int) -> int:
    max_score = 0
    best_quantities = None

    for quantities in _get_quantities(volume, len(ingredients)):
        cur_calories = _get_calories(ingredients, quantities)
        if cur_calories != calories:
            continue

        score = _get_score(ingredients, quantities)
        if score > max_score:
            max_score = score
            best_quantities = quantities

    return best_quantities, max_score


def _get_quantities(volume: int, n: int) -> Iterable:
    for values in product(range(1, volume), repeat=n):
        if sum(values) == volume:
            yield values


def _get_score(ingredients: list[Ingredient], quantities: tuple[int]) -> int:
    score = 1
    for prop in ["capacity", "durability", "flavor", "texture"]:
        score *= _get_prop_score(ingredients, quantities, prop)
    return score


def _get_calories(ingredients: list[Ingredient], quantities: tuple[int]) -> int:
    return _get_prop_score(ingredients, quantities, "calories")


def _get_prop_score(ingredients, quantities, prop) -> int:
    prop_score = 0
    for q, i in zip(quantities, ingredients):
        prop_score += q * getattr(i, prop)
    return max(0, prop_score)


ingredients = [
    Ingredient("Butterscotch", -1, -2, 6, 3, 8),
    Ingredient("Cinnamon", 2, 3, -2, -1, 3),
]
assert (_get_score(ingredients, [1, 1])) == (-1 + 2) * (-2 + 3) * (6 - 2) * (3 - 1)
assert (_get_score(ingredients, [2, 1])) == 0
assert (_get_score(ingredients, [3, 1])) == 0

assert list(_get_quantities(3, 2)) == [(1, 2), (2, 1)]

assert max_score(ingredients, volume=100, calories=500) == ((40, 60), 57_600_000)


with open("2015/15_science_for_hungry_people/input.txt") as f:
    spec = (
        "{name}: capacity {capacity:d}, durability {durability:d}, flavor {flavor:d}, "
        "texture {texture:d}, calories {calories:d}"
    )
    ingredients = [Ingredient(**parse(spec, line.strip()).named) for line in f]

    print(max_score(ingredients, volume=100, calories=500))
