#!/usr/bin/env python3
import sys
from collections import defaultdict


class Number:
    def __init__(self, string, current_index, part=False):
        self.value = int(string)
        self.end = current_index - 1
        self.start = current_index - len(string)
        self.part = part

    def __str__(self):
        return "%d (%d -> %d) [%s]" % (self.value, self.start, self.end, "yes" if self.part else "no")


def extract(line):
    numbers = []
    symbols = []
    stars = []
    cur = ""
    index = 0
    for char in line.strip():
        if char.isnumeric():
            cur += char

        else:
            if char != ".":
                if len(cur) > 0:
                    numbers.append(Number(cur, index, True))
                symbols.append(index)

                if char == "*":
                    stars.append(index)

            elif len(cur) > 0:
                numbers.append(Number(cur, index))

            cur = ""

        index += 1

    if len(cur) > 0:
        numbers.append(Number(cur, index))

    return [numbers, symbols, stars]


def flag_parts(numbers, symbols, stars):
    if len(numbers) == 0 or len(symbols) == 0:
        return

    symbol_index = 0
    symbol = symbols[symbol_index]
    number_index = 0
    number = numbers[number_index]
    start = symbol - 1
    end = symbol + 1
    star = symbol in stars
    while number:
        if number.start > end:
            symbol_index += 1
            if symbol_index >= len(symbols):
                return

            symbol = symbols[symbol_index]
            start = symbol - 1
            end = symbol + 1
            star = symbol in stars

        else:
            if number.start >= start or (number.start < start and number.end >= start):
                number.part = True

                if star:
                    stars[symbol].append(number)

            number_index += 1
            if number_index >= len(numbers):
                return

            number = numbers[number_index]


with open(sys.argv[1], "r") as f:
    numbers_grid = []
    symbols_grid = []
    stars_grid = defaultdict(dict)
    index = 0
    for line in f:
        numbers, symbols, stars = extract(line)
        numbers_grid.append(numbers)
        symbols_grid.append(symbols)

        for star in stars:
            stars_grid[index][star] = []

        index += 1

    for x in range(len(numbers_grid)):
        if x > 0:
            flag_parts(numbers_grid[x-1], symbols_grid[x], stars_grid[x])

        flag_parts(numbers_grid[x], symbols_grid[x], stars_grid[x])

        if x < (len(numbers_grid) - 1):
            flag_parts(numbers_grid[x+1], symbols_grid[x], stars_grid[x])

    total = 0
    index = 0
    for numbers in numbers_grid:
        for number in numbers:
            if number.part:
                total += number.value

        index += 1

    gear = 0
    for x in stars_grid:
        for y in stars_grid[x]:
            if len(stars_grid[x][y]) == 2:
                gear += stars_grid[x][y][0].value * stars_grid[x][y][1].value

    print(total)
    print(gear)
