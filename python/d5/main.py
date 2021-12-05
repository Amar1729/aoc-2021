#! /usr/bin/env python3

import collections
import sys
from pprint import pprint


def parse_lines(lines):
    """
    Returns list up 2-tuples of begin+end points
    """
    points = []
    for l in lines:
        p1_pre, p2_pre = l.split(" -> ")
        p1 = tuple(map(int, p1_pre.split(",")))
        p2 = tuple(map(int, p2_pre.split(",")))

        points.append((p1, p2))

    return points


def line_generator(p1, p2):
    """
    Generates all points between p1 and p2
    """
    assert p1 != p2
    slope = (p1[0] - p2[0], p1[1] - p2[1])

    if slope[0] == 0:
        # normalize
        slope = (slope[0], slope[1] // abs(slope[1]))
    elif slope[1] == 0:
        slope = (slope[0] // abs(slope[0]), slope[1])

    curr = p1
    yield curr

    # assumes curr will get to p2
    while curr != p2:
        curr = (curr[0] - slope[0], curr[1] - slope[1])
        yield curr


def p1(lines):
    manhattan_lines = list(filter(lambda ps: ps[0][0] == ps[1][0] or ps[0][1] == ps[1][1], parse_lines(lines)))

    freq_grid = collections.defaultdict(int)

    for p1, p2 in manhattan_lines:
        # print(p1, p2)
        # pprint(list(line_generator(p1, p2)))
        # print()
        for p in line_generator(p1, p2):
            freq_grid[p] += 1

    return len(list(filter(lambda v: v > 1, freq_grid.values())))


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
