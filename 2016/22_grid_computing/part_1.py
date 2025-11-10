"""
You gain access to a massive storage cluster arranged in a grid;
each storage node is only connected to the four nodes directly adjacent to it
(three if the node is on an edge, two if it's in a corner).

You can directly access data only on node /dev/grid/node-x0-y0,
but you can perform some limited actions on the other nodes:

-   You can get the disk usage of all nodes (via df).
    The result of doing this is in your puzzle input.
-   You can instruct a node to move (not copy) all of its data to an adjacent node
    (if the destination node has enough space to receive the data).
    The sending node is left empty after this operation.

Nodes are named by their position:
the node named node-x10-y10 is adjacent to nodes
node-x9-y10, node-x11-y10, node-x10-y9, and node-x10-y11.

Before you begin, you need to understand the arrangement of data on these nodes.
Even though you can only move data between directly connected nodes,
you're going to need to rearrange a lot of the data to get access to the data you need.
Therefore, you need to work out how you might be able to shift data around.

To do this, you'd like to count the number of viable pairs of nodes.
A viable pair is any two nodes (A,B),
regardless of whether they are directly connected, such that:

- Node A is not empty (its Used is not zero).
- Nodes A and B are not the same node.
- The data on node A (its Used) would fit on node B (its Avail).

How many viable pairs of nodes are there?
"""

from dataclasses import dataclass
from itertools import combinations

from parse import parse


@dataclass(kw_only=True)
class Node:
    x: int = 0
    y: int = 0
    total: int = 0
    used: int = 0
    available: int = 0
    percent: int = 0


def get_viable_pairs(nodes: list[Node]) -> list[Node]:
    viable_pairs = []
    for node_1, node_2 in combinations(nodes, 2):
        node_1_fits = node_1.used and node_1.used <= node_2.available
        node_2_fits = node_2.used and node_2.used <= node_1.available
        if node_1_fits or node_2_fits:
            viable_pairs.append((node_1, node_2))
    return viable_pairs


def _parse_node(raw_node: str) -> Node:
    spec = (
        "/dev/grid/node-x{x:d}-y{y:d}{total:>d}T{used:>d}T{available:>d}T{percent:>d}%"
    )
    return Node(**parse(spec, raw_node).named)


node_1 = Node(used=1, available=1)
node_2 = Node(used=1, available=1)
assert get_viable_pairs([node_1, node_2]) == [(node_1, node_2)]

node_1 = Node(used=0, available=1)
node_2 = Node(used=0, available=1)
assert get_viable_pairs([node_1, node_2]) == []

with open("2016/22_grid_computing/input.txt") as f:
    next(f)
    next(f)

    nodes = [_parse_node(line.strip()) for line in f]
    print(len(get_viable_pairs(nodes)))
