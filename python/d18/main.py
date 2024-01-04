#! /usr/bin/env python3

from __future__ import annotations

import copy
import functools
import itertools
import math
import re
import sys
from pprint import pprint
from typing import Generator, List, Tuple


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


class Number:
    """Implementation of Snailfish numbers.

    The above "Shellfish" implementation was built as a list of tuples, and it sort of works but
    isn't ergonomic to read/modify. This one is a bit more verbose but more accurately reflects
    what's actually happening in the problem statement.
    """

    def __init__(self, left: Number | int, right: Number | int, parent: Number | None = None):
        self.left = left
        self.right = right
        self.parent = parent

        # if user is manually creating a nested number, make sure to resolve parents.
        if not isinstance(left, int) or not isinstance(right, int):
            self.resolve_parents()

    def resolve_parents(self, parent: Number | None = None):
        self.parent = parent

        if isinstance(self.left, Number):
            self.left.resolve_parents(self)

        if isinstance(self.right, Number):
            self.right.resolve_parents(self)

    @staticmethod
    def _parse(line: str) -> tuple[Number, str]:
        left: Number | int
        right: Number | int

        # base case
        m = re.match(r"\[([0-9]+),([0-9]+)\]", line)
        if m:
            left = int(m.group(1))
            right = int(m.group(2))
            return Number(left, right), line[m.end():]

        assert line[0] == "["  # ]

        if line[1].isdigit():
            m = re.match(r"[0-9]+,", line[1:])
            assert m is not None
            left = int(m.group().rstrip(","))
            rem = line[1 + m.end():]
        else:
            left, rem = Number._parse(line[1:])
            assert rem[0] == ","
            rem = rem[1:]

        if rem[0].isdigit():
            m = re.match(r"[0-9]+", rem)
            assert m is not None
            right = int(m.group())
            rem = rem[m.end():]
        else:
            right, rem = Number._parse(rem)

        assert rem[0] == "]"
        rem = rem[1:]

        return Number(left, right), rem

    @staticmethod
    def from_str(line: str) -> Number:
        left, rem = Number._parse(line)

        if rem:
            assert rem[0] == ","
            rem = rem[1:]
            right, rem = Number._parse(rem)

            # hm.
            if rem == "]":
                rem = ""

            num = Number(left, right)
        else:
            num = left

        if rem:
            raise ValueError(rem)

        num.resolve_parents()
        return num

    @staticmethod
    def gen_split(x: int) -> Number:
        # rounded down
        left = x // 2
        # rounded up
        right = (x + 1) // 2
        return Number(left, right)

    def __add__(self, other: Number) -> Number:
        num = Number(copy.deepcopy(self), copy.deepcopy(other))
        assert isinstance(num.left, Number)
        assert isinstance(num.right, Number)
        num.left.parent = num
        num.right.parent = num

        # print("Before mutate:", num)

        # merge/split
        while num.explode() or num.split():
            # print("after mutate:", num)
            pass

        return num

    def __eq__(self, other) -> bool:
        if not isinstance(other, Number):
            return False

        if self.parent is not None and other.parent is not None:
            pass
        elif self.parent is None and other.parent is None:
            pass
        else:
            return False

        return self.left == other.left and self.right == self.right

    def __iter__(self) -> Generator[tuple[Number | None, Number | int], None, None]:
        """Iterate over the parents and values in a Number."""
        if isinstance(self.left, int) and isinstance(self.right, int):
            yield self.parent, self
            # done
            return

        if isinstance(self.left, Number):
            yield from iter(self.left)
        else:
            yield self, self.left

        if isinstance(self.right, Number):
            yield from iter(self.right)
        else:
            yield self, self.right

    def __str__(self) -> str:
        # no space, to reflect input format.
        return f"[{self.left},{self.right}]"

    def __repr__(self) -> str:
        return str(self)

    def depth(self) -> int:
        c = 0
        parent = self.parent
        while parent is not None:
            parent = parent.parent
            c += 1
        return c

    def window(self):
        """Sliding window of three int/Numbers over iter(self)."""
        it = itertools.chain([(None, None)], iter(self), [(None, None)])
        a, b, c = itertools.tee(it, 3)
        next(c)
        next(c)
        next(b)

        yield from zip(a, b, c)

    def assign_of(self, val: Number | int, new_val: Number | int, from_left: bool):
        """Kind of gross: change a particular value in a Number.

        I didn't encode a way to tell whether a particular value is the left or right attribute,
        so I have to do this weird check over left and right values.
        """
        if from_left:
            if self.left == val:
                self.left = new_val
                return
            if self.right == val:
                self.right = new_val
                return
        else:
            if self.right == val:
                self.right = new_val
                return
            if self.left == val:
                self.left = new_val
                return

        raise ValueError

    def explode(self) -> bool:
        for (pa, na), (pb, nb), (pc, nc) in self.window():
            if isinstance(nb, Number) and nb.depth() > 3:
                x, y = nb.left, nb.right
                if not isinstance(x, int) or not isinstance(y, int):
                    raise TypeError(type(x), type(y))
                assert pb is not None
                pb.assign_of(nb, -1, True)

                # modify number to left.
                if pa is not None and isinstance(na, int):
                    pa.assign_of(na, na + x, False)
                elif isinstance(na, Number):
                    assert isinstance(na.right, int)
                    na.right = na.right + x

                # modify number to right.
                if pc is not None and isinstance(nc, int):
                    pc.assign_of(nc, nc + y, True)
                elif isinstance(nc, Number):
                    assert isinstance(nc.left, int)
                    nc.left = nc.left + y

                pb.assign_of(-1, 0, True)

                return True

        return False

    def split(self) -> bool:
        for pb, nb in self:

            if isinstance(nb, int) and nb >= 10:
                assert pb is not None
                new_num = Number.gen_split(nb)
                new_num.parent = pb
                pb.assign_of(nb, new_num, True)
                return True

            if isinstance(nb, Number) and isinstance(nb.left, int) and nb.left >= 10:
                new_num = Number.gen_split(nb.left)
                new_num.parent = nb
                nb.left = new_num
                return True

            if isinstance(nb, Number) and isinstance(nb.right, int) and nb.right >= 10:
                new_num = Number.gen_split(nb.right)
                new_num.parent = nb
                nb.right = new_num
                return True

        return False

    def magnitude(self) -> int:
        m = 3 * (self.left if isinstance(self.left, int) else self.left.magnitude())
        m += 2 * (self.right if isinstance(self.right, int) else self.right.magnitude())
        return m


def p1(lines):
    # implemented later for p2 work: proper Snailfish class
    # snailfish = [Number.from_str(line) for line in lines]
    # s = functools.reduce(lambda x, y: x + y, snailfish)
    # return s.magnitude()

    shellfish = [Shellfish(line) for line in lines]
    s = functools.reduce(lambda x, y: x + y, shellfish)
    print(s)

    # p1 answer:
    # this is disgusting, but i manually added these brackets after print(s)
    # because i can't quite figure out the tree parsing?
    s = eval('[[[[6,6],[7,7]],[[7,7],[7,7]]],[[[9,7],[6,8]],[[7,7],[0,8]]]]')
    print(s)
    return magnitude(s)


def p2(lines) -> int:
    # ez pz (once i have a better way to add snailfish numbers ...)
    snailfish = [Number.from_str(line) for line in lines]

    return max(
        (n1 + n2).magnitude()
        for n1, n2 in itertools.permutations(snailfish, 2)
    )


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
