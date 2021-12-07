#! /usr/bin/env python3

import sys


def median(numbers):
    l = sorted(numbers)
    if len(l) % 2 == 0:
        return (l[len(l) // 2] + l[len(l) // 2 - 1]) / 2
    else:
        return l[len(l) // 2]


def p1(lines):
    positions = list(map(int, lines[0].strip().split(",")))

    # geometric mean of 1d numbers is median:
    meeting = int(median(positions))
    return sum(abs(p - meeting) for p in positions)


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
