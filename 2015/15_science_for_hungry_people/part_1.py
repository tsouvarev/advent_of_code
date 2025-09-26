"""
Today, you set out on the task of perfecting your milk-dunking cookie recipe.
All you have to do is find the right balance of ingredients.

Your recipe leaves room for exactly 100 teaspoons of ingredients.
You make a list of the remaining ingredients you could use
to finish the recipe (your puzzle input) and their properties per teaspoon:

- capacity (how well it helps the cookie absorb milk)
- durability (how well it keeps the cookie intact when full of milk)
- flavor (how tasty it makes the cookie)
- texture (how it improves the feel of the cookie)
- calories (how many calories it adds to the cookie)

You can only measure ingredients in whole-teaspoon amounts accurately,
and you have to be accurate so you can reproduce your results in the future.
The total score of a cookie can be found by adding up
each of the properties (negative totals become 0)
and then multiplying together everything except calories.

For instance, suppose you have these two ingredients:

- Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
- Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of cinnamon
(because the amounts of each ingredient must add up to 100)
would result in a cookie with the following properties:

- A capacity of 44*-1 + 56*2 = 68
- A durability of 44*-2 + 56*3 = 80
- A flavor of 44*6 + 56*-2 = 152
- A texture of 44*3 + 56*-1 = 76

Multiplying these together (68 * 80 * 152 * 76, ignoring calories for now)
results in a total score of 62842880,
which happens to be the best score possible given these ingredients.
If any properties had produced a negative total, it would have instead become zero,
causing the whole score to multiply to zero.

Given the ingredients in your kitchen and their properties,
what is the total score of the highest-scoring cookie you can make?
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


def max_score(ingredients: list[Ingredient], volume: int) -> int:
    max_score = 0
    best_quantities = None

    for quantities in _get_quantities(volume, len(ingredients)):
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
        prop_score = 0
        for q, i in zip(quantities, ingredients):
            prop_score += q * getattr(i, prop)
        score *= max(0, prop_score)
    return score


ingredients = [
    Ingredient("Butterscotch", -1, -2, 6, 3, 8),
    Ingredient("Cinnamon", 2, 3, -2, -1, 3),
]
assert (_get_score(ingredients, [1, 1])) == (-1 + 2) * (-2 + 3) * (6 - 2) * (3 - 1)
assert (_get_score(ingredients, [2, 1])) == 0
assert (_get_score(ingredients, [3, 1])) == 0

assert list(_get_quantities(3, 2)) == [(1, 2), (2, 1)]

assert max_score(ingredients, volume=100) == ((44, 56), 62_842_880)


with open("2015/15_science_for_hungry_people/input.txt") as f:
    spec = (
        "{name}: capacity {capacity:d}, durability {durability:d}, flavor {flavor:d}, "
        "texture {texture:d}, calories {calories:d}"
    )
    ingredients = [Ingredient(**parse(spec, line.strip()).named) for line in f]
    print(max_score(ingredients, volume=100))
