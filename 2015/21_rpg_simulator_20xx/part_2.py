"""
Turns out the shopkeeper is working with the boss,
and can persuade you to buy whatever items he wants.
The other rules still apply, and he still only has one of each item.

What is the most amount of gold you can spend and still lose the fight?
"""

from dataclasses import dataclass
from itertools import product
from math import ceil


@dataclass
class Item:
    name: str
    cost: int
    stats: "Stats"


@dataclass
class Player:
    health: int
    stats: "Stats"
    items: list[Item]

    @property
    def damage(self):
        return sum(i.stats.damage for i in self.items) + self.stats.damage

    @property
    def armor(self):
        return sum(i.stats.armor for i in self.items) + self.stats.armor

    @property
    def cost(self):
        return sum(i.cost for i in self.items)


@dataclass
class Stats:
    damage: int
    armor: int


WEAPONS = [
    Item("Dagger", 8, Stats(4, 0)),
    Item("Shortsword", 10, Stats(5, 0)),
    Item("Warhammer", 25, Stats(6, 0)),
    Item("Longsword", 40, Stats(7, 0)),
    Item("Greataxe", 74, Stats(8, 0)),
]

ARMOR = [
    None,
    Item("Leather", 13, Stats(0, 1)),
    Item("Chainmail", 31, Stats(0, 2)),
    Item("Splintmail", 53, Stats(0, 3)),
    Item("Bandedmail", 75, Stats(0, 4)),
    Item("Platemail", 102, Stats(0, 5)),
]

LEFT_RINGS = [
    None,
    Item("Damage +1", 25, Stats(1, 0)),
    Item("Damage +2", 50, Stats(2, 0)),
    Item("Damage +3", 100, Stats(3, 0)),
]

RIGHT_RINGS = [
    None,
    Item("Defense +1", 20, Stats(0, 1)),
    Item("Defense +2", 40, Stats(0, 2)),
    Item("Defense +3", 80, Stats(0, 3)),
]

BOSS = Player(104, Stats(8, 1), items=[])


def find_equipment() -> tuple[int, list[Item]]:
    max_cost = 0
    max_items = []

    all_possible_items = product(WEAPONS, ARMOR, LEFT_RINGS, RIGHT_RINGS)

    for possible_items in all_possible_items:
        items = [i for i in possible_items if i]
        player = Player(100, Stats(0, 0), items=items)

        if not _can_player_win(boss=BOSS, player=player) and player.cost > max_cost:
            max_cost = player.cost
            max_items = player.items

    return max_cost, max_items


def _can_player_win(boss: Player, player: Player) -> bool:
    boss_power = max(1, boss.damage - player.armor)
    player_power = max(1, player.damage - boss.armor)

    boss_rounds_to_win = ceil(player.health / boss_power)
    player_rounds_to_win = ceil(boss.health / player_power)

    return player_rounds_to_win <= boss_rounds_to_win


def _fight(b, p, items=None):
    if items is None:
        items = []
    boss_health, *boss_stats = b
    boss = Player(boss_health, Stats(*boss_stats), items=[])

    player_health, *player_stats = p
    player = Player(
        player_health,
        stats=Stats(*player_stats),
        items=[Item(1, 1, Stats(*spec)) for spec in items],
    )

    return _can_player_win(boss, player)


assert _fight(b=(1, 1, 0), p=(1, 1, 0)) is True
assert _fight(b=(2, 2, 0), p=(1, 1, 0)) is False
assert _fight(b=(1, 1, 1), p=(1, 1, 1)) is True
assert _fight(b=(2, 2, 1), p=(2, 2, 1)) is True

assert _fight(b=(104, 8, 1), p=(100, 9, 0)) is True
assert _fight(b=(104, 8, 1), p=(100, 4, 5)) is False

assert _fight(b=(2, 1, 0), p=(1, 1, 1), items=[(1, 0)]) is True

print(find_equipment())
