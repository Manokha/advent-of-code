#!/usr/bin/env python3
import sys
from collections import defaultdict


def parse_part(part):
    return list(map(int, part.strip().replace("  ", " ").split(" ")))

def parse(line):
    winning, available = map(parse_part, line.strip().split(": ", 1)[1].split(" | ", 1))
    matches = 0
    for number in available:
        if number in winning:
            matches += 1

    return matches


with open(sys.argv[1], "r") as f:
    card = 1
    total = 0
    copies = defaultdict(int)
    for line in f:
        matches = parse(line)
        if matches > 0:
            total += pow(2, matches - 1)

            factor = 1 + copies[card]
            for copy in range(card + 1, card + matches + 1):
                copies[copy] += factor

        card += 1

    card -= 1
    count = card
    for copy in copies:
        if copy <= card:
            count += copies[copy]

    print(total)
    print(count)
