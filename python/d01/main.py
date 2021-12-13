#! /usr/bin/env python3

import sys
import itertools


def p1(fname):
    prev = None
    count = 0
    with open(fname) as f:
        for line in f.readlines():
            curr = int(line.strip())

            if prev:
                if curr > prev:
                    count += 1
            prev = curr

    return count


def p2(fname):
    with open(fname) as f:
        meas = map(lambda e: int(e.strip()), f.readlines())

    a, b, c = itertools.tee(iter(meas), 3)
    next(b)
    next(c); next(c)

    slidings = [sum(s) for s in zip(a, b, c)]
    count = 0
    prev = slidings[0]
    for s in slidings[1:]:
        if s > prev:
            count += 1
        prev = s

    return count


if __name__ == "__main__":
    print(p2(sys.argv[1]))
