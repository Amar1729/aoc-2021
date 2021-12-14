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
    # horrendously naive for p1, RIP
    polymer = lines[0]
    rules = dict((pair.strip().split(" -> ") for pair in lines[2:]))

    c = collections.Counter(map(str.__add__, polymer, polymer[1:]))
    num_p = collections.Counter(polymer)

    def step(c):
        new_c = collections.defaultdict(int)
        for pair, value in c.items():
            p = rules[pair]
            new_c[pair[0] + p] += value
            new_c[p + pair[1]] += value
            num_p[p] += value

        return new_c

    for _ in range(40):
        c = step(c)

    s = sorted(num_p.items(), key=lambda x: x[1], reverse=True)
    return(s[0][1] - s[-1][1])


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
