#! /usr/bin/env python3

import sys
import math
from functools import lru_cache


def median(numbers):
    l = sorted(numbers)
    if len(l) % 2 == 0:
        return (l[len(l) // 2] + l[len(l) // 2 - 1]) / 2
    else:
        return l[len(l) // 2]


@lru_cache
def triangular(n):
    if n == 0:
        return 0
    else:
        return sum(i for i in range(n+1))


def p1(lines):
    positions = list(map(int, lines[0].strip().split(",")))

    # geometric mean of 1d numbers is median:
    meeting = int(median(positions))
    return sum(abs(p - meeting) for p in positions)


def p2(lines):
    positions = sorted(list(map(int, lines[0].strip().split(","))))

    avg = sum(positions) / len(positions)
    fuel_low = sum(triangular(abs(p - math.floor(avg))) for p in positions)
    fuel_high = sum(triangular(abs(p - math.ceil(avg))) for p in positions)
    return min(fuel_low, fuel_high)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
