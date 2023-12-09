#!/usr/bin/env python3
import sys
import re


class Parser:
    def __init__(self):
        self.next_values = []
        self.previous_values = []

    def parse(self, line):
        values = list(map(int, re.findall('-?\d+', line)))
        current = []
        next_sequence = [values[-1]]
        previous_sequence = [values[0]]

        while len(values) > 1:
            stop = True

            for i in range(1, len(values)):
                diff = values[i] - values[i-1]

                if diff != 0:
                    stop = False

                current.append(diff)

            if stop:
                break

            values = current
            current = []
            next_sequence.append(values[-1])
            previous_sequence.append(values[0])


        self.next_values.append(sum(next_sequence))

        cur = previous_sequence[-1]
        for i in range(len(previous_sequence) - 2, -1, -1):
            cur = previous_sequence[i] - cur

        self.previous_values.append(cur)

    def compute_next(self):
        return sum(self.next_values)

    def compute_previous(self):
        return sum(self.previous_values)


with open(sys.argv[1], "r") as f:
    parser = Parser()
    for line in f:
        parser.parse(line)

    print(parser.compute_next())
    print(parser.compute_previous())
