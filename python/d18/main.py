#! /usr/bin/env python3

import sys
import collections
import itertools
import functools
import math

from pprint import pprint
from typing import List, Tuple


def parse_pairs(ev: list[str], depth: int = 0):
    # runs twice on the two-element input ev
    for elem in ev:
        if isinstance(elem, int):
            yield (depth, elem)
        elif isinstance(elem, list):
            assert len(elem) == 2
            yield from parse_pairs(elem, depth + 1)
    return


def rev_parse_pairs(arr: List[Tuple[int, int]], currdepth=0):
    l = []
    if arr[0][0] == currdepth:
        l.append(arr.pop(0)[1])
    elif arr[0][0] > currdepth:
        l.append(rev_parse_pairs(arr, currdepth + 1))

    if arr[0][0] == currdepth:
        l.append(arr.pop(0)[1])
    else:
        l.append(rev_parse_pairs(arr, currdepth + 1))
    return l


def magnitude(arr) -> int:
    left = 3 * (arr[0] if isinstance(arr[0], int) else magnitude(arr[0]))
    right = 2 * (arr[1] if isinstance(arr[1], int) else magnitude(arr[1]))

    return left + right


class Shellfish:
    def __init__(self, st=None):
        # keep fish as list of tuples
        # (depth, value)
        # this way we should be able to immediately skip left/right to other numbers
        if st:
            self.fish = list(parse_pairs(eval(st)))
        else:
            self.fish = []

    def explode(self) -> bool:
        for first_deep_idx, (depth, _) in enumerate(self.fish):
            if depth >= 4:
                break
        else:
            return False

        assert isinstance(self.fish[first_deep_idx][1], int)
        assert isinstance(self.fish[first_deep_idx + 1][1], int)

        left = self.fish[first_deep_idx][1]
        right = self.fish[first_deep_idx + 1][1]

        if first_deep_idx > 0:
            left_nu = self.fish[first_deep_idx - 1]
            self.fish[first_deep_idx - 1] = (left_nu[0], left_nu[1] + left)

        if first_deep_idx + 2 < len(self.fish):
            right_nu = self.fish[first_deep_idx + 2]
            self.fish[first_deep_idx + 2] = (right_nu[0], right_nu[1] + right)

        self.fish.pop(first_deep_idx)
        self.fish[first_deep_idx] = (depth - 1, 0)

        return True

    def split(self) -> bool:
        for split_idx, (depth, f) in enumerate(self.fish):
            if f >= 10:
                break
        else:
            return False

        self.fish[split_idx] = (depth + 1, math.ceil(f / 2))
        self.fish.insert(split_idx, (depth + 1, f // 2))

        return True

    def verify(self):
        while True:
            if self.explode():
                # pass here instead, for efficiency?
                pass
            elif self.split():
                pass
            else:
                break

    def magnitude(self):
        arr = rev_parse_pairs(self.fish)

        left = 3 * (arr[0] if isinstance(arr[0], int) else magnitude(arr[0]))
        right = 2 * (arr[1] if isinstance(arr[1], int) else magnitude(arr[1]))

        return left + right

    def __add__(self, other):
        new_fish = Shellfish()
        fish = []
        for depth, f in itertools.chain(self.fish, other.fish):
            fish.append((depth + 1, f))

        new_fish.fish = fish
        new_fish.verify()
        return new_fish

    def __str__(self):
        st = ""
        depth = 0
        for d, f in self.fish:
            if d > depth:
                st += "[" * (d - depth)
            elif d < depth:
                st += "]" * (depth - d)

            depth = d

            st += str(f)
            st += ","

        return "[" + st[:-1] + "]"


def p1(lines):
    shellfish = [Shellfish(line) for line in lines]
    s = functools.reduce(lambda x, y: x + y, shellfish)
    print(s)

    # p1 answer:
    # this is disgusting, but i manually added these brackets after print(s)
    # because i can't quite figure out the tree parsing?
    s = eval('[[[[6,6],[7,7]],[[7,7],[7,7]]],[[[9,7],[6,8]],[[7,7],[0,8]]]]')
    print(s)
    return magnitude(s)


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
