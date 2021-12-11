#! /usr/bin/env python3

import copy
import sys
import collections
import itertools
import functools
import math

from pprint import pprint


def print_grid(lines, grid):
    for y, row in enumerate(lines):
        st = "".join([str(grid[complex(x, y)]) for x, v in enumerate(row)])
        print(st)


def p1(lines):
    grid = {
        complex(x, y): int(v)
        for y, row in enumerate(lines)
        for x, v in enumerate(row)
    }

    num_flashes = 0

    offsets = [
        complex(1, 0),
        complex(-1, 0),
        complex(0, 1),
        complex(0, -1),

        complex(-1, -1),
        complex(-1, 1),
        complex(1, -1),
        complex(1, 1),
    ]

    def neighbors(p, g):
        for off in offsets:
            if p + off in g:
                yield p + off

    for step in range(100):
        new_grid = {}
        to_flash = set()
        flashed = set()
        for p, v in grid.items():
            new_grid[p] = v + 1
            if v + 1 > 9:
                to_flash.add(p)

        while to_flash:
            curr = to_flash.pop()
            flashed.add(curr)

            num_flashes += 1

            for n in neighbors(curr, grid):
                if n not in flashed:
                    new_grid[n] += 1
                    if new_grid[n] > 9:
                        if n not in to_flash:
                            to_flash.add(n)

        for p in new_grid:
            if new_grid[p] > 9:
                new_grid[p] = 0

        grid = new_grid

    return num_flashes


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
