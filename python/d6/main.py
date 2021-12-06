#! /usr/bin/env python3

import sys


def p1(lines):
    fish = list(map(int, lines[0].split(",")))

    new_fish = []
    for _ in range(80):
        for i in range(len(fish)):
            if fish[i] == 0:
                fish[i] = 6
                new_fish.append(8)
            else:
                fish[i] -= 1

        while new_fish:
            fish.append(new_fish.pop(0))

    return len(fish)


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
