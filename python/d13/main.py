#! /usr/bin/env python3

import sys
import collections
import itertools
import functools
import math

from pprint import pprint


def p1(lines, p2=False):
    d = set()
    for idx, p in enumerate(lines):
        if not p:
            break
        x, y = map(int, p.split(","))
        d.add((x, y))

    folds = list(map(lambda l: l.split()[-1].split("="), lines[idx+1:]))

    for direction, value in folds:
        new_d = set()
        for x, y in d:
            if direction == "y" and y > int(value):
                new_d.add((x, int(value) - (y - int(value))))
            elif direction == "x" and x > int(value):
                new_d.add((int(value) - (x - int(value)), y))
            else:
                new_d.add((x, y))

        d = new_d
        if not p2:
            return len(d)

    return d


def p2(lines):
    d = p1(lines, True)

    max_x = max(d, key=lambda p: p[0])[0]
    max_y = max(d, key=lambda p: p[1])[1]

    return "\n".join([
        "".join(map(lambda x: "#" if (x, y) in d else ".", range(max_x + 1)))
        for y in range(max_y + 1)
    ])


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
