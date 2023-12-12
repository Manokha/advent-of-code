#!/usr/bin/env python3
import sys


class Parser:
    def __init__(self):
        self.total = 0

    def parse(self, line):
        positions, groups = line.split(" ")
        groups = list(map(int, groups.split(',')))

        print("")
        print("  %s %s" % (positions, groups))

        result = self.compute(positions, groups)
        print("=", result)
        print("")
        self.total += result

    def compute(self, positions, groups, prefix=""):
        if not len(groups):
            return 1

        if len(positions) < groups[0]:
            return 0

        # print(">", prefix + positions, groups)

        next_prefix = prefix

        i = 0
        size = groups[0]
        mandatory = False

        for position in positions:
            if (position == "?" or position == "#") and (len(positions) <= (i + size) or positions[i + size] != "#"):
                size -= 1
                if position == "#":
                    mandatory = True

                if size == 0:
                    if len(positions) > (i + 1) and positions[i + 1] == "#":
                        if (i - groups[0] + 1) >= 0 and positions[i - groups[0] + 1] == "?":
                            next_prefix += "?"
                        else:
                            size = groups[0]
                            next_prefix += "." + positions[i - groups[0] + 1:i]
                    else:
                        if len(groups) == 1:
                            invalid = "#" in positions[i + 1:]

                            if not invalid:
                                print("-", next_prefix + ("#" * groups[0]) + positions[i + 1:])

                            return (0 if invalid else 1) + (0 if positions[i - groups[0] + 1] == "#" else self.compute(
                                positions[i - groups[0] + 2:],
                                groups,
                                next_prefix + "."
                            ))

                        return self.compute(
                            positions[i + 2:],
                            groups[1:],
                            next_prefix + (("#" * groups[0]) + ".")
                        ) + (0 if positions[i - groups[0] + 1] == "#" else self.compute(
                            positions[i - groups[0] + 2:],
                            groups,
                            next_prefix + "."
                        ))

            else:
                if position == "#":
                    return 0

                if size < groups[0]:
                    if mandatory:
                        return 0

                    next_prefix += positions[i - groups[0] + size:i]
                    size = groups[0]

                next_prefix += "."

            i += 1

        return 0

with open(sys.argv[1], "r") as f:
    parser = Parser()

    for line in f:
        parser.parse(line)

    print("")
    print(parser.total)
