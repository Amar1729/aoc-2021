#! /usr/bin/env python3

import sys
import collections
import itertools
import functools
import math

from pprint import pprint


bad_map = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def parse(line):
    pda = []

    for c in line:
        if c in "([{<":
            pda.append(c)
        else:
            if c == ")":
                if pda[-1] == "(":
                    pda.pop(len(pda)-1)
                else:
                    return False, (pda[-1], ")")
            elif c == "}":
                if pda[-1] == "{":
                    pda.pop(len(pda)-1)
                else:
                    return False, (pda[-1], "}")
            elif c == ">":
                if pda[-1] == "<":
                    pda.pop(len(pda)-1)
                else:
                    return False, (pda[-1], ">")
            elif c == "]":
                if pda[-1] == "[":
                    pda.pop(len(pda)-1)
                else:
                    return False, (pda[-1], "]")

    return True, (len(pda), 0)


def p1(lines):
    return sum(
        bad_map[v]
        for k, (_, v) in [parse(line) for line in lines]
        if not k
    )


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
