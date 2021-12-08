#! /usr/bin/env python3

import sys
import collections
import itertools

"""
0 - 6
1 - 2
2 - 5
3 - 5
4 - 4
5 - 5
6 - 6
7 - 3
8 - 7
9 - 6
"""


def p1(lines):
    return sum(
        len(list(filter(
            lambda w: len(w) in [2, 4, 3, 7],
            [word for word in output.split(" | ")[1].split()]
        )))
        for output in lines
    )


def p2(lines):
    pass


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()

    print(p1(lines))
    print(p2(lines))
