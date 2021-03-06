#! /usr/bin/env python3

import sys
import collections
import itertools
import functools
import math

from heapq import heapify, heappush, heappop
from pprint import pprint


def neighbors(point, grid):
    for x, y in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        p = point + complex(x, y)
        if p in grid:
            yield p


def transform_grid(grid):
    new_grid = {}

    x_off = max([int(p.real) for p in grid]) + 1
    y_off = max([int(p.imag) for p in grid]) + 1

    for c, v in grid.items():
        for x in range(5):
            for y in range(5):
                offset = complex(x_off * x, y_off * y)
                np = c + offset
                nv = v + x + y
                while nv > 9:
                    nv -= 9

                new_grid[np] = nv

    return new_grid


def p1(lines, p2=False):
    grid = {
        complex(x, y): int(value)
        for y, row in enumerate(lines)
        for x, value in enumerate(row)
    }

    entry_point = complex(0, 0)
    last_point = complex(len(lines[0])-1, len(lines)-1)

    if p2:
        grid = transform_grid(grid)
        x = max([int(p.real) for p in grid]) + 1
        y = max([int(p.imag) for p in grid]) + 1
        last_point = complex(x - 1, y - 1)

    costs = {}  # keep track of visited -> lowest score, path
    queue = []  # bfs queue

    costs[entry_point] = (0, [])
    heappush(queue, (0, [entry_point]))

    while queue:
        score, path = queue.pop(0)
        point = path[-1]

        if point == last_point:
            continue

        for np in neighbors(point, grid):
            # print("point:", point, "neighbor:", np)
            if np not in costs:
                p = (grid[np] + costs[point][0], costs[point][1] + [np])
                try:
                    heappush(queue, p)
                except TypeError:
                    pass

                costs[np] = p
            else:
                if point in costs:
                    cost = grid[np] + costs[point][0]
                    if cost < costs[np][0]:
                        costs[np] = (cost, path + [np])
                        try:
                            heappush(queue, costs[np])
                        except TypeError:
                            pass

    return costs[last_point][0]


def p2(lines):
    return p1(lines, True)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
