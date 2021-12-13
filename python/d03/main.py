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
    o2 = None
    co2 = None

    o2_nums = [l.strip() for l in lines]
    co2_nums = [l.strip() for l in lines]

    def partition(step, lines, tiebreak):
        if not lines:
            # return []
            pass
        freq = collections.defaultdict(int)
        column = list(zip(*lines))[step]
        for bit in column:
            freq[bit] += 1

        if freq["0"] > freq["1"]:
            most_common = "0"
        # elif freq["1"] >= freq["0"]:
        else:
            most_common = "1"

        if tiebreak == "1":
            return list(filter(lambda l: l[step] == most_common, lines))
        else:
            return list(filter(lambda l: l[step] != most_common, lines))

    for step in range(len(o2_nums[0])):

        if not o2:
            o2_nums = partition(step, o2_nums, "1")

            if len(o2_nums) == 1:
                o2 = o2_nums[0]

        if not co2:
            co2_nums = partition(step, co2_nums, "0")

            if len(co2_nums) == 1:
                co2 = co2_nums[0]

        if o2 and co2:
            break

    return int(o2, 2) * int(co2, 2)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    # print(p1(lines))
    print(p2(lines))
