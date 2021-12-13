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
        return len(d)


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
