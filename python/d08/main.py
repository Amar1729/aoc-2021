#! /usr/bin/env python3

import sys
import copy
import collections
import itertools

from typing import Optional, List
# from pprint import pprint

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


class Segment:
    def __init__(self):
        # top-left to bottom-right:
        # each part has a set of possibilities
        self.parts = {i: set("abcdefg") for i in range(7)}

        self.part_map = {
            0: [0, 1, 2, 4, 5, 6],
            1: [2, 5],
            2: [0, 2, 3, 4, 6],
            3: [0, 2, 3, 5, 6],
            4: [1, 2, 3, 5],
            5: [0, 1, 3, 5, 6],
            6: [0, 1, 3, 4, 5, 6],
            7: [0, 2, 5],
            8: list(range(7)),
            9: [0, 1, 2, 3, 5, 6],
        }

        self.rev_parts = {}

    def _update_all_but(self, part):
        # this part is solved, remove its soln from other parts
        for x in [_ for _ in range(7) if _ != part]:
            prev = len(self.parts[x])
            self.parts[x] = self.parts[x] - self.parts[part]

            if prev > 1 and len(self.parts[x]) == 1:
                self._update_all_but(x)

    def update(self, digit, chars):
        for i in self.part_map[digit]:
            prev = len(self.parts[i])
            self.parts[i] &= set(chars)

            if prev > 1 and len(self.parts[i]) == 1:
                self._update_all_but(i)

        # if part[i] has three possibilities that overlap with part[x]
        # which has only two, then we can solve part[i] (it's the only
        # option remaing)
        for i in self.part_map[digit]:
            for v in self.parts.values():
                if len(self.parts[i] & v) == 1:
                    self.parts[i] = self.parts[i] & v

        # remove the possibilities for this part from all the parts not
        # of this digit (e.g. 0/1/3/4/6 for digit 1)
        for x in [_ for _ in range(7) if _ not in self.part_map[digit]]:
            self.parts[x] -= set(chars)

    def verify(self) -> bool:
        # ensure we didn't update to a bad state
        parts = list(self.parts.items())
        for idx, (_, v) in enumerate(parts):
            if not v:
                return False

            for _, v2 in parts[:idx] + parts[idx+1:]:
                if len(v) == 1 and v == v2:
                    return False

        return True

    def get_digit(self, chars) -> int:
        # get digit from input chars
        if not self.rev_parts:
            self.rev_parts = {v.pop(): k for k, v in self.parts.items()}

        parts = sorted([self.rev_parts[c] for c in chars])
        return next(filter(lambda pm: pm[1] == parts, self.part_map.items()))[0]

    def __str__(self):
        return str(self.parts)


def p1(lines):
    return sum(
        len(list(filter(
            lambda w: len(w) in [2, 4, 3, 7],
            [word for word in output.split(" | ")[1].split()]
        )))
        for output in lines
    )


def det_seg(inp: List[str], s: Segment, d5_combo, d6_combo) -> Optional[Segment]:
    for idx, d5_p in enumerate(filter(lambda w: len(w) == 5, inp)):
        s.update(d5_combo[idx], d5_p)

        if not s.verify():
            return None

    for idx, d6_p in enumerate(filter(lambda w: len(w) == 6, inp)):
        s.update(d6_combo[idx], d6_p)

        if not s.verify():
            return None

    return s


def solve(signals: List[str], numbers: List[str], segment: Segment):
    for d6_c in itertools.permutations([0, 6, 9]):
        for d5_c in itertools.permutations([2, 3, 5]):
            seg = copy.deepcopy(segment)

            # print(d5_c, d6_c)

            if s := det_seg(signals, seg, d5_c, d6_c):
                # pprint(s.parts)
                for n in numbers:
                    yield s.get_digit(n)

                return


def p2(lines):

    total = 0

    for display in lines:

        inp, output = display.split(" | ")
        signals = inp.split()
        numbers = output.split()

        segment = Segment()

        d_1 = next(filter(lambda w: len(w) == 2, signals))
        d_4 = next(filter(lambda w: len(w) == 4, signals))
        d_7 = next(filter(lambda w: len(w) == 3, signals))

        segment.update(1, d_1)
        segment.update(4, d_4)
        segment.update(7, d_7)

        value = int("".join(map(str, solve(signals, numbers, segment))))
        total += value

    return total


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()

    # print(p1(lines))
    print(p2(lines))
