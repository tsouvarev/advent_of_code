"""
This year is the Reindeer Olympics!
Reindeer can fly at high speeds, but must rest occasionally to recover their energy.
Santa would like to know which of his reindeer is fastest, and so he has them race.

Reindeer can only either be flying (always at their top speed)
or resting (not moving at all), and always spend whole seconds in either state.

For example, suppose you have the following Reindeer:

    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

After one second, Comet has gone 14 km, while Dancer has gone 16 km.
After ten seconds, Comet has gone 140 km, while Dancer has gone 160 km.
On the eleventh second, Comet begins resting (staying at 140 km),
and Dancer continues on for a total distance of 176 km.
On the 12th second, both reindeer are resting.
They continue to rest until the 138th second, when Comet flies for another ten seconds.
On the 174th second, Dancer flies for another 11 seconds.

In this example, after the 1000th second, both reindeer are resting,
and Comet is in the lead at 1120 km (poor Dancer has only gotten 1056 km by that point).
So, in this situation, Comet would win (if the race ended at 1000 seconds).

Given the descriptions of each reindeer (in your puzzle input),
after exactly 2503 seconds, what distance has the winning reindeer traveled?
"""

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import islice


@dataclass
class Racer:
    name: str
    speed: int
    racing_for_seconds: int
    resting_for_seconds: int


def race(racers: list[Racer], seconds: int) -> tuple[Racer, int]:
    best_racer = None
    max_distance = 0

    for racer in racers:
        track = _build_racer_track(racer)
        distance = sum(islice(track, seconds))

        if distance > max_distance:
            max_distance = distance
            best_racer = racer

    return best_racer, max_distance


def _build_racer_track(racer: Racer) -> Iterable[int]:
    while True:
        yield from [racer.speed for _ in range(racer.racing_for_seconds)]
        yield from [0 for _ in range(racer.resting_for_seconds)]


racers = [Racer("Comet", 14, 10, 127), Racer("Dancer", 16, 11, 162)]
assert race(racers, 1000) == (Racer("Comet", 14, 10, 127), 1120)


with open("2015/14_reindeer_olympics/input.txt") as f:
    racers = []
    for line in f:
        "Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds."
        tokens = line.split(" ")
        racer = Racer(tokens[0], int(tokens[3]), int(tokens[6]), int(tokens[13]))
        racers.append(racer)

    print(race(racers, 2503))
