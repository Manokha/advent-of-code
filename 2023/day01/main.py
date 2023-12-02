#!/usr/bin/env python3
import sys

def get_first_digit(line):
    for char in line:
        if char.isnumeric():
            return char

def extract_two_digits(line):
    return int(get_first_digit(line) + get_first_digit(reversed(line)))


replace_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def replace(line):
    result = line
    for label in replace_map:
        result = result.replace(label, label + replace_map[label] + label)

    return result

with open(sys.argv[1], "r") as f:
    total = 0
    for line in f:
        total += extract_two_digits(replace(line))

    print(total)
