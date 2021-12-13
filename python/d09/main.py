#! /usr/bin/env python3

import sys
import collections
import itertools
import functools

from pprint import pprint


class HMap:
    def __init__(self, grid):
        self.grid = grid
        self.explored = set()

    def lows(self):
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                if self.check_adjecent(x, y):
                    yield (x, y), value

    def check_adjecent(self, x, y) -> bool:
        point = self.grid[y][x]

        if x > 0:
            if self.grid[y][x-1] <= point:
                return False

        if x < len(self.grid[y])-1:
            if self.grid[y][x+1] <= point:
                return False

        if y > 0:
            if self.grid[y-1][x] <= point:
                return False

        if y < len(self.grid)-1:
            if self.grid[y+1][x] <= point:
                return False

        return True

    def check_yield(self, x, y):
        if (x, y) not in self.explored:
            self.explored.add((x, y))
            yield (x, y)
            yield from self.explore(x, y)

    def explore(self, x, y):
        # given x, y, keep exploring until we hit an edge or 9
        if x > 0:
            if self.grid[y][x-1] < 9:
                yield from self.check_yield(x-1, y)

        if x < len(self.grid[y])-1:
            if self.grid[y][x+1] < 9:
                yield from self.check_yield(x+1, y)

        if y > 0:
            if self.grid[y-1][x] < 9:
                yield from self.check_yield(x, y-1)

        if y < len(self.grid)-1:
            if self.grid[y+1][x] < 9:
                yield from self.check_yield(x, y+1)


def p1(lines):
    hmap = HMap([list(map(int, [c for c in row])) for row in lines])
    return sum(map(lambda x: x[1]+1, hmap.lows()))


def p2(lines):
    hmap = HMap([list(map(int, [c for c in row])) for row in lines])

    basin_sizes = sorted(list(len(list(hmap.explore(x, y))) for (x, y), _ in hmap.lows()))
    return functools.reduce(lambda x, y: x * y, basin_sizes[-3:])


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
