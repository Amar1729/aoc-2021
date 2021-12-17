#! /usr/bin/env python3

import sys
import collections
import itertools
import functools
import math

from pprint import pprint


def px(x, t):
    return sum(x - s for s in range(min(t, x)))


def py(y, t):
    return sum(y - s for s in range(t))


def vys(vy_i, y_min=-math.inf):
    # yield every velocity_y given initial vy
    # until position (assumed to start from 0) reaches y_min
    y_curr = 0
    vy = vy_i
    yield vy
    while y_curr > y_min:
        y_curr += vy
        vy -= 1
        yield vy


def find_yt(py_range, vy):
    # finds time t at which starting velocity vy gives position py
    for t, y in enumerate(vys(vy, py_range[0])):
        if y in py_range:
            yield t


def p1(lines):
    tx, ty = lines[0].split(": ")[1].split(", ")
    txi, txf = list(map(int, tx.split("=")[1].split("..")))
    tyi, tyf = list(map(int, ty.split("=")[1].split("..")))

    x_range = range(txi, txf + 1)
    y_range = range(tyi, tyf + 1)

    valid_xs = []
    for x in range(x_range[-1]):
        if px(x, x) >= x_range[0]:
            valid_xs.append(x)

    max_vy = abs(y_range[0]) - 1  # smallest y is the first coord
    vy = max_vy

    while True:  # loop until we find a solution
        print(f"finding: {vy}")
        for t in find_yt(y_range, vy):
            for x in valid_xs:
                if px(x, t) in x_range:
                    # print(x, vy)
                    # yth triangle number (max height)
                    return py(vy, vy)
        vy -= 1


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
