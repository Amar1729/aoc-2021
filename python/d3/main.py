#! /usr/bin/env python3

import collections
import sys


def p1(lines):
    gamma, epsilon = ("", "")

    for column in zip(*map(lambda l: l.strip(), lines)):
        freq = collections.defaultdict(int)
        for bit in column:
            freq[bit] += 1

        if freq["0"] > freq["1"]:
            gamma += "0"
            epsilon += "1"
        else:
            epsilon += "0"
            gamma += "1"

    return int(gamma, 2) * int(epsilon, 2)


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    print(p1(lines))
    # print(p2(lines))
