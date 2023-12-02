#!/usr/bin/env python3
import sys
from collections import defaultdict


red_cubes = 12
green_cubes = 13
blue_cubes = 14

def extract_data(line):
    index = line.find(":")
    game = defaultdict(int)
    game["id"] = int(line[5:index])
    for game_set in line[index+2:].split("; "):
        for cubes_count in game_set.split(", "):
            count, color = cubes_count.strip().split(" ")
            game[color] = max(int(count), game[color])

    return game


with open(sys.argv[1], "r") as f:
    total = 0
    power = 0
    for line in f:
        game = extract_data(line)
        if game["red"] <= red_cubes and game["green"] <= green_cubes and game["blue"] <= blue_cubes:
            total += game["id"]

        power += game["red"] * game["green"] * game["blue"]

    print(total)
    print(power)
