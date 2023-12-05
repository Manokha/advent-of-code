#!/usr/bin/env python3
import sys
from collections import defaultdict


class Converter:
    def __init__(self, dest_range_start, src_range_start, length):
        self.start = src_range_start
        self.end = src_range_start + length - 1
        self.diff = dest_range_start - src_range_start

class Parser:
    def __init__(self):
        self.seeds = []
        self.maps = []
        self.index = -1

    def parse(self, raw_line):
        line = raw_line.strip()
        if line.startswith("seeds: "):
            self.seeds = list(map(int, line[7:].split(" ")))

        elif line.endswith(" map:"):
            self.index += 1
            self.maps.append([])

        elif len(line) > 0:
            self.maps[self.index].append(Converter(*map(int, line.split(" "))))

    def get_location(self):
        result = None
        for seed in self.seeds:
            location = seed
            for converters in self.maps:
                for converter in converters:
                    if location >= converter.start and location <= converter.end:
                        location += converter.diff
                        break

            if result is None:
                result = location
            else:
                result = min(result, location)

        return result

    def get_range_loccation(self):
        cur_ranges = list(map(lambda seed_range: (seed_range[0], seed_range[0] + seed_range[1] - 1), zip(self.seeds[::2], self.seeds[1::2])))
        for converters in self.maps:
            converted_ranges = []
            cur_index = 0
            max_index = len(cur_ranges)

            while cur_index < max_index:
                start, end = cur_ranges[cur_index]
                for converter in converters:
                    if start >= converter.start and start <= converter.end:
                        if end <= converter.end:
                            start += converter.diff
                            end += converter.diff
                            break

                        else:
                            converted_ranges.append((start + converter.diff, converter.end + converter.diff))
                            start = converter.end + 1

                    elif start < converter.start and end >= converter.start:
                        if end <= converter.end:
                            converted_ranges.append((converter.start + converter.diff, end + converter.diff))
                            end = converter.start - 1

                        else:
                            converted_ranges.append((converter.start + converter.diff, converter.end + converter.diff))
                            cur_ranges.append((converter.end + 1, end))
                            max_index += 1
                            end = converter.start - 1

                if start <= end:
                    converted_ranges.append((start, end))

                cur_index += 1

            cur_ranges = converted_ranges

        return min(map(lambda location_range: location_range[0], cur_ranges))

with open(sys.argv[1], "r") as f:
    parser = Parser()

    for line in f:
        parser.parse(line)

    print(parser.get_location())
    print(parser.get_range_loccation())
