"""
Seeing how reindeer move in bursts,
Santa decides he's not pleased with the old scoring system.

Instead, at the end of each second,
he awards one point to the reindeer currently in the lead.
(If there are multiple reindeer tied for the lead, they each get one point.)
He keeps the traditional 2503 second time limit, of course,
as doing otherwise would be entirely ridiculous.

Given the example reindeer from above, after the first second,
Dancer is in the lead and gets one point.
He stays in the lead until several seconds into Comet's second burst:
after the 140th second, Comet pulls into the lead and gets his first point.
Of course, since Dancer had been in the lead for the 139 seconds before that,
he has accumulated 139 points by the 140th second.

After the 1000th second, Dancer has accumulated 689 points,
while poor Comet, our old champion, only has 312.
So, with the new scoring system, Dancer would win (if the race ended at 1000 seconds).

Again given the descriptions of each reindeer (in your puzzle input),
after exactly 2503 seconds, how many points does the winning reindeer have?
"""

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class Racer:
    name: str
    speed: int
    racing_for_seconds: int
    resting_for_seconds: int


def race(racers: list[Racer], seconds: int) -> dict:
    tracks = {racer.name: _build_racer_track(racer) for racer in racers}
    distances = dict.fromkeys(tracks, 0)
    scores = dict.fromkeys(tracks, 0)

    for _ in range(seconds):
        max_distance = 0

        for name, track in tracks.items():
            distances[name] += next(track)
            max_distance = max(distances[name], max_distance)

        for name, distance in distances.items():
            if distance == max_distance:
                scores[name] += 1

    return scores


def _build_racer_track(racer: Racer) -> Iterable[int]:
    while True:
        yield from [racer.speed for _ in range(racer.racing_for_seconds)]
        yield from [0 for _ in range(racer.resting_for_seconds)]


racers = [Racer("Comet", 14, 10, 127), Racer("Dancer", 16, 11, 162)]
assert race(racers, 1000) == {"Comet": 312, "Dancer": 689}


with open("2015/14_reindeer_olympics/input.txt") as f:
    racers = []
    for line in f:
        tokens = line.split(" ")
        racer = Racer(tokens[0], int(tokens[3]), int(tokens[6]), int(tokens[13]))
        racers.append(racer)

    print(race(racers, 2503))
