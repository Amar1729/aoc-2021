#! /usr/bin/env python3

import sys


def det_die():
    while True:
        for c in range(1, 101):
            yield c


def p1(lines):
    # i see there's a closed form that fits the players' scores ...
    # might be worth to impl. in part 2 if necessary, but naive is fast
    # enough for part 1
    p1 = int(lines[0].split(" ")[-1])
    p2 = int(lines[1].split(" ")[-1])

    score_1 = 0
    score_2 = 0

    d = det_die()
    roll_count = 0

    while score_1 < 1000 and score_2 < 1000:
        s = sum(next(d) for _ in range(3))
        p1 += s
        p1 = p1 % 10
        if p1 == 0:
            p1 = 10
        score_1 += p1

        roll_count += 3

        # print(f"Player 1 rolls {s} and moves to space {p1} for total score {score_1}")

        if score_1 >= 1000:
            break

        s = sum(next(d) for _ in range(3))
        p2 += s
        p2 = p2 % 10
        if p2 == 0:
            p2 = 10
        score_2 += p2

        roll_count += 3

        # print(f"Player 2 rolls {s} and moves to space {p2} for total score {score_2}")

    if score_1 < 1000:
        return roll_count * score_1
    else:
        return roll_count * score_2


def p2(lines):
    pass


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()
    print(p1(lines))
    # print(p2(lines))
