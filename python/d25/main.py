#! /usr/bin/env python3

import sys


def p1(lines):
    cucs = {
        (x, y): v
        for y, row in enumerate(lines)
        for x, v in enumerate(row)
        if v in ">v"
    }

    max_x = len(lines[0])
    max_y = len(lines)

    c = 1

    while True:
        new_cucs = {}
        moved = False

        for point, cuc in cucs.items():
            if cuc == ">":
                if point[0] == max_x - 1:
                    nx = 0
                else:
                    nx = point[0] + 1
                nx = (point[0] + 1) % max_x

                if (nx, point[1]) not in cucs:
                    new_cucs[(nx, point[1])] = cuc
                    moved = True
                else:
                    new_cucs[point] = cuc

        for point, cuc in cucs.items():
            if cuc == "v":
                ny = (point[1] + 1) % max_y

                np = (point[0], ny)
                if cucs.get(np, "") == "v":
                    new_cucs[point] = cuc
                elif new_cucs.get(np, "") == ">":
                    new_cucs[point] = cuc
                else:
                    new_cucs[np] = cuc
                    moved = True

        if not moved:
            return c

        cucs = new_cucs
        c += 1


def p2(lines):
    pass


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()
    print(p1(lines))
    # print(p2(lines))
