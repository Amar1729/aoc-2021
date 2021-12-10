#! /usr/bin/env python3

import sys
import collections
import itertools
import functools
import math

from pprint import pprint
from statistics import median


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

    return True, (len(pda), pda)


def p1(lines):
    return sum(
        bad_map[v]
        for k, (_, v) in [parse(line) for line in lines]
        if not k
    )


def p2(lines):
    chr_score = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4,
    }

    scores = [
        functools.reduce(
            lambda x, y: x * 5 + chr_score[y],
            pda[::-1],
            0,
        )
        for k, (_, pda) in map(parse, lines)
        if k
    ]

    return(median(scores))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
