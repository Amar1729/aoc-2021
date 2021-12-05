#! /usr/bin/env python3

import sys


def p1(lines):
    x = 0
    z = 0

    for instr in lines:
        direction, value = instr.strip().split()

        if direction == "forward":
            x += int(value)
        elif direction == "down":
            z += int(value)
        elif direction == "up":
            z -= int(value)

    return x * z


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    print(p1(lines))
    # print(p2(lines))
