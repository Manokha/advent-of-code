#!/usr/bin/env python3
import sys


class Galaxy:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class Parser:
    def __init__(self):
        self.galaxies = []
        self.col_empty = None
        self.y = 0
        self.expansion = 2

    def parse(self, line):
        x = 0
        empty = True

        if self.col_empty is None:
            self.col_empty = [True for _ in line.strip()]

        for char in line:
            if char == '#':
                self.galaxies.append(Galaxy(str(len(self.galaxies) + 1), x, self.y))
                empty = False
                self.col_empty[x] = False

            x += 1

        self.y += self.expansion if empty else 1

    def compute(self):
        incr = []
        cur = 0
        for x in range(len(self.col_empty)):
            if self.col_empty[x]:
                cur += self.expansion - 1

            incr.append(cur)

        total = 0

        for galaxy in self.galaxies:
            galaxy.x += incr[galaxy.x]

        for i in range(len(self.galaxies)):
            galaxy = self.galaxies[i]
            for j in range(i + 1, len(self.galaxies)):
                target = self.galaxies[j]
                total += abs(target.x - galaxy.x) + abs(target.y - galaxy.y)

        return total


with open(sys.argv[1], "r") as f:
    parser = Parser()
    if len(sys.argv) > 2:
        parser.expansion = int(sys.argv[2])

    for line in f:
        parser.parse(line)

    print(parser.compute())
