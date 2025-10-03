"""
Little Henry Case got a new video game for Christmas.
It's an RPG, and he's stuck on a boss.
He needs to know what equipment to buy at the shop. He hands you the controller.

In this game, the player (you) and the enemy (the boss) take turns attacking.
The player always goes first.
Each attack reduces the opponent's hit points by at least 1.
The first character at or below 0 hit points loses.

Damage dealt by an attacker each turn
is equal to the attacker's damage score minus the defender's armor score.
An attacker always does at least 1 damage.
So, if the attacker has a damage score of 8,
and the defender has an armor score of 3, the defender loses 5 hit points.
If the defender had an armor score of 300, the defender would still lose 1 hit point.

Your damage score and armor score both start at zero.
They can be increased by buying items in exchange for gold.
You start with no items and have as much gold as you need.
Your total damage or armor is equal to the sum of those stats from all of your items.
You have 100 hit points.

Here is what the item shop is selling:

Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3

You must buy exactly one weapon; no dual-wielding.
Armor is optional, but you can't use more than one.
You can buy 0-2 rings (at most one for each hand).
You must use any items you buy. The shop only has one of each item,
so you can't buy, for example, two rings of Damage +3.

For example,
suppose you have 8 hit points, 5 damage, and 5 armor,
and that the boss has 12 hit points, 7 damage, and 2 armor:

    The player deals 5-2 = 3 damage; the boss goes down to 9 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 6 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 6 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 4 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 3 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 2 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 0 hit points.

In this scenario, the player wins! (Barely.)

You have 100 hit points. The boss's actual stats are in your puzzle input.
What is the least amount of gold you can spend and still win the fight?
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
    min_cost = 1_000_000
    min_items = []

    all_possible_items = product(WEAPONS, ARMOR, LEFT_RINGS, RIGHT_RINGS)

    for possible_items in all_possible_items:
        items = [i for i in possible_items if i]
        player = Player(100, Stats(0, 0), items=items)

        if _can_player_win(boss=BOSS, player=player) and player.cost < min_cost:
            min_cost = player.cost
            min_items = player.items

    return min_cost, min_items


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
