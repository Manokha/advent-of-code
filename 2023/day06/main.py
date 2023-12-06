#!/usr/bin/env python3
import re
import sys
from collections import defaultdict


class Parser:
    def __init__(self):
        self.times = []
        self.distances = []

        self.time = 0
        self.distance = 0

    def parse(self, line):
        if line.startswith("Time: "):
            times = re.findall('\d+', line)
            self.times = list(map(int, times))
            self.time = int("".join(times))
        elif line.startswith("Distance: "):
            distances = re.findall('\d+', line)
            self.distances = list(map(int, distances))
            self.distance = int("".join(distances))

    def compute(self):
        total = 0
        i = 0
        while i < len(self.times):
            result = self.compute_one(self.times[i], self.distances[i])
            if total == 0:
                total = result
            else:
                total *= result

            i += 1

        return total

    def compute_one(self, duration, record):
        speed = int(duration / 2)
        dist = speed * (duration - speed)
        prev = (speed - 1) * (duration - speed + 1)
        too_low = 0
        too_high = speed

        while dist < record or prev > record:
            if dist < record:
                too_low = speed
                speed += int((too_high - speed) / 2)
            else:
                too_high = speed
                speed -= int((speed - too_low) / 2)

            dist = speed * (duration - speed)
            prev = (speed - 1) * (duration - speed + 1)

        return duration + 1 - (2 * speed)


with open(sys.argv[1], "r") as f:
    parser = Parser()

    for line in f:
        parser.parse(line)

    print(parser.compute())
    print(parser.compute_one(parser.time, parser.distance))
