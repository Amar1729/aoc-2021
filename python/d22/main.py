#! /usr/bin/env python3

import sys


def parse_directions(lines):
    for line in lines:
        power, ranges = line.split(" ")
        rs = []
        for r in ranges.split(","):
            _r = r.split("=")[1].split("..")
            ri = int(_r[0])
            rf = int(_r[-1]) + 1
            if ri < -50:
                ri = -50
            if rf > 50:
                rf = 51
            rs.append(range(ri, rf))

        yield (True if power == "on" else False, rs)


def p1(lines):
    # i think a set of 3-tuples will be too slow for p2

    cubes = set()

    for power, ranges in parse_directions(lines):
        # print(power, ranges)

        # c = 0

        for x in ranges[0]:
            for y in ranges[1]:
                for z in ranges[2]:
                    if -50 <= x <= 50 and -50 <= y <= 50 and -50 <= z <= 50:
                        if power:
                            if (x, y, z) not in cubes:
                                # c += 1
                                pass
                            cubes.add((x, y, z))
                        else:
                            p = (x, y, z)
                            if p in cubes:
                                # c -= 1
                                cubes.remove(p)

        # print(f"{c} cubes")
        # print()

    return len(cubes)


def p2(lines):
    pass


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()

    print(p1(lines))
    # print(p2(lines))
