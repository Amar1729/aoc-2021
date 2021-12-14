#! /usr/bin/env python3

import sys
import collections
import itertools
import functools
import math

from pprint import pprint


def p1(lines):
    polymer = lines[0]

    # rules = lines[2:]
    rules = {
        line.split(" -> ")[0]: line.split(" -> ")[1]
        for line in lines[2:]
    }

    for _ in range(40):
        a, b = itertools.tee(iter(polymer))

        st = ""
        st += next(b)

        for first, second in zip(a, b):
            st += rules[first + second]
            st += second

        polymer = st

    c = collections.Counter(polymer)
    common = c.most_common(1)[0][1]
    c2 = sorted(c.items(), key=lambda x: x[1], reverse=True)
    common = c2[0][1]
    least = c2[-1][1]

    return common - least


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
