#!/usr/bin/env python3
import sys


shapes = {
    "|": [True, True, False, False],
    "-": [False, False, True, True],
    "L": [True, False, False, True],
    "J": [True, False, True, False],
    "7": [False, True, True, False],
    "F": [False, True, False, True],
    ".": [False, False, False, False],
    "S": [True, True, True, True],
}

class Node:
    def __init__(self, shape, line, row):
        self.shape = shape
        self.line = line
        self.row = row
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.dist = None

        self.inc_north = False
        self.inc_south = False
        self.inc_west = False
        self.inc_east = False

class Parser:
    def __init__(self):
        self.nodes = []
        self.previous = None
        self.line = 0
        self.row = 0
        self.start_node = None

    def parse(self, line):
        self.row = 0
        self.nodes.append(list(map(self.parse_node, line.strip())))
        self.line += 1

    def parse_node(self, shape):
        node = Node(shape, self.line, self.row)
        if shape == "S":
            self.start_node = node
            node.dist = 0

        if shapes[shape][0] and self.line > 0 and shapes[self.nodes[self.line - 1][self.row].shape][1]:
            node.north = self.nodes[self.line - 1][self.row]
            node.north.south = node
        if shapes[shape][2] and self.row > 0 and shapes[self.previous.shape][3]:
            node.west = self.previous
            self.previous.east = node

        self.row += 1
        self.previous = node
        return node

    def compute(self):
        paths = [node for node in [self.start_node.north, self.start_node.south, self.start_node.west, self.start_node.east] if node is not None]
        dist = 1

        while len(paths) > 0:
            nexts = []

            for node in paths:
                node.dist = dist

                node_paths = [n for n in [node.north, node.south, node.west, node.east] if n is not None and (n.dist is None or n.dist > (dist + 1))]
                if len(node_paths) == 1:
                    nexts.append(node_paths[0])

            paths = nexts
            dist += 1

        return dist - 1

    def compute_enclosed(self):
        count = 0
        first = self.get_first_loop_node()
        first.inc_south = True
        first.inc_east = True

        [current, direction] = self.east(first)

        while current is not first:
            if current.inc_east and current.east is None:
                row = current.row + 1
                while self.nodes[current.line][row].dist is None:
                    count += 1
                    row += 1

            [current, direction] = direction(current)

        return count

    def get_first_loop_node(self):
        for nodes_list in self.nodes:
            for node in nodes_list:
                if node.dist is not None:
                    return node

    def east(self, previous):
        current = previous.east
        current.inc_north = current.north is not None or previous.inc_north
        current.inc_south = current.south is not None or previous.inc_south
        current.inc_east = current.east is not None or (previous.inc_south and current.north is not None) or (previous.inc_north and current.south is not None)
        current.inc_west = not current.inc_east
        return [current, self.north if current.north is not None else self.south if current.south is not None else self.east]

    def south(self, previous):
        current = previous.south
        current.inc_south = current.south is not None or (previous.inc_east and current.west is not None) or (previous.inc_west and current.east is not None)
        current.inc_north = not current.inc_south
        current.inc_west = current.west is not None or previous.inc_west
        current.inc_east = current.east is not None or previous.inc_east
        return [current, self.south if current.south is not None else self.west if current.west is not None else self.east]

    def north(self, previous):
        current = previous.north
        current.inc_north = current.north is not None or (previous.inc_east and current.west is not None) or (previous.inc_west and current.east is not None)
        current.inc_south = not current.inc_north
        current.inc_west = current.west is not None or previous.inc_west
        current.inc_east = current.east is not None or previous.inc_east
        return [current, self.north if current.north is not None else self.west if current.west is not None else self.east]

    def west(self, previous):
        current = previous.west
        current.inc_north = current.north is not None or previous.inc_north
        current.inc_south = current.south is not None or previous.inc_south
        current.inc_west = current.west is not None or (previous.inc_south and current.north is not None) or (previous.inc_north and current.south is not None)
        current.inc_east = not current.inc_west
        return [current, self.north if current.north is not None else self.south if current.south is not None else self.west]


with open(sys.argv[1], "r") as f:
    parser = Parser()
    for line in f:
        parser.parse(line)

    print(parser.compute())
    print(parser.compute_enclosed())
