#!/usr/bin/env python3
import sys
from math import lcm


class Node:
    def __init__(self, left, right):
        self.L = left
        self.R = right

class Map:
    def __init__(self):
        self.instructions = None
        self.nodes = {}
        self.starting_nodes = []

    def parse_instructions(self, line):
        self.instructions = line.strip()

    def parse_node(self, line):
        key = line[0:3]
        self.nodes[key] = Node(line[7:10], line[12:15])
        if key.endswith("A"):
            self.starting_nodes.append(key)

    def compute(self):
        current = "AAA"
        steps = 0
        while current != "ZZZ":
            for instruction in self.instructions:
                current = getattr(self.nodes[current], instruction)

                steps += 1

                if current == "ZZZ":
                    break

        return steps

    def compute_ghost(self):
        currents = list(self.starting_nodes)
        steps = 0
        goods = []
        size = len(currents)

        while len(goods) < size:
            for instruction in self.instructions:
                steps += 1
                for i in range(size):
                    if not currents[i].endswith("Z"):
                        currents[i] = getattr(self.nodes[currents[i]], instruction)
                        if currents[i].endswith("Z"):
                            goods.append(steps)

                if len(goods) >= size:
                    break

        return lcm(*goods)


with open(sys.argv[1], "r") as f:
    m = Map()
    m.parse_instructions(f.readline())
    # Skip empty line
    f.readline()
    for line in f:
        m.parse_node(line)

    print(m.compute())
    print(m.compute_ghost())
