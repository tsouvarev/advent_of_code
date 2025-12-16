"""
You hear some loud beeping coming from a hatch in the floor of the factory,
so you decide to check it out.
Inside, you find several large electrical conduits and a ladder.

Climbing down the ladder, you discover the source of the beeping:
a large, toroidal reactor which powers the factory above.
Some Elves here are hurriedly running between the reactor and a nearby server rack,
apparently trying to fix something.

One of the Elves notices you and rushes over.
"It's a good thing you're here! We just installed a new server rack,
but we aren't having any luck getting the reactor to communicate with it!"
You glance around the room and see a tangle of cables
and devices running from the server rack to the reactor.
She rushes off, returning a moment later
with a list of the devices and their outputs (your puzzle input).

For example:

aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out

Each line gives the name of a device followed by a list of the devices
to which its outputs are attached. So, bbb: ddd eee means
that device bbb has two outputs, one leading to device ddd
and the other leading to device eee.

The Elves are pretty sure that the issue isn't due to any specific device,
but rather that the issue is triggered by data
following some specific path through the devices.
Data only ever flows from a device through its outputs; it can't flow backwards.

After dividing up the work,
the Elves would like you to focus on the devices starting with the one next to you
(an Elf hastily attaches a label which just says you)
and ending with the main output to the reactor (which is the device with the label out).

To help the Elves figure out which path is causing the issue,
they need you to find every path from you to out.

In this example, these are all of the paths from you to out:

    Data could take the connection from you to bbb, then from bbb to ddd,
    then from ddd to ggg, then from ggg to out.
    Data could take the connection to bbb, then to eee, then to out.
    Data could go to ccc, then ddd, then ggg, then out.
    Data could go to ccc, then eee, then out.
    Data could go to ccc, then fff, then out.

In total, there are 5 different paths leading from you to out.

How many different paths lead from you to out?
"""

from collections import defaultdict, deque

type Path = list[Device]
type Device = str

START, END = "you", "out"


def find_paths(raw_devices: list[str]) -> set[Path]:
    devices_map = _parse_devices(raw_devices)
    res = set()

    queue = deque([[START]])

    while queue:
        *history, device = queue.pop()

        for next_device in devices_map[device]:
            path = (*history, device, next_device)

            if next_device == END:
                res.add(path)
            elif next_device not in path[:-1]:
                queue.append(path)

    return res


def _parse_devices(raw_devices: list[str]) -> dict[Device, list[Device]]:
    res = defaultdict(list)
    for raw_device in raw_devices:
        from_, to_ = raw_device.split(": ")
        res[from_] = to_.split(" ")
    return res


assert _parse_devices(["aaa: you hhh"]) == {"aaa": ["you", "hhh"]}

devices = [
    "aaa: you hhh",
    "you: bbb ccc",
    "bbb: ddd eee",
    "ccc: ddd eee fff",
    "ddd: ggg",
    "eee: out",
    "fff: out",
    "ggg: out",
    "hhh: ccc fff iii",
    "iii: out",
]
assert find_paths(devices) == {
    ("you", "bbb", "ddd", "ggg", "out"),
    ("you", "bbb", "eee", "out"),
    ("you", "ccc", "ddd", "ggg", "out"),
    ("you", "ccc", "eee", "out"),
    ("you", "ccc", "fff", "out"),
}


with open("2025/11_reactor/input.txt") as f:
    lines = [line.strip() for line in f]
    print(len(find_paths(lines)))
