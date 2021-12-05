#! /usr/bin/env python3

import sys


def p1(fname):
    prev = None
    count = 0
    with open(fname) as f:
        for line in f.readlines():
            curr = int(line.strip())

            if prev:
                if curr > prev:
                    count += 1
            prev = curr

    return count


if __name__ == "__main__":
    print(p1(sys.argv[1]))
