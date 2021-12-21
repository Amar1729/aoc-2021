#! /usr/bin/env python3

import collections
import functools
import itertools
import sys


# for p2
LIMIT = 21
MOVEMENT = collections.Counter([sum(p) for p in itertools.product([1, 2, 3], repeat=3)])


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


@functools.lru_cache(maxsize=512)
def recurse(score_1: int, score_2: int, curr_1: int, curr_2: int, p1: bool = True):
    # this function could probably be written slightly better ...
    if p1:
        if score_1 == 20:
            # all rolls win here
            return (27, 0)
        else:
            wins = [0, 0]
            for idx_1, q in [(curr_1 + m, q) for m, q in MOVEMENT.items()]:
                if idx_1 > 10:
                    idx_1 -= 10
                s_1 = score_1 + idx_1
                if s_1 >= LIMIT:
                    wins[0] += (1 * q)
                else:
                    sc = recurse(score_1 + idx_1, score_2, idx_1, curr_2, False)
                    wins[0] += sc[0] * q
                    wins[1] += sc[1] * q
            return tuple(wins)

    else:
        if score_2 == 20:
            return (0, 27)
        else:
            wins = [0, 0]
            for idx_2, q in [(curr_2 + m, q) for m, q in MOVEMENT.items()]:
                if idx_2 > 10:
                    idx_2 -= 10
                s_2 = score_2 + idx_2
                if s_2 >= LIMIT:
                    wins[1] += 1 * q
                else:
                    sc = recurse(score_1, score_2 + idx_2, curr_1, idx_2, True)
                    wins[0] += sc[0] * q
                    wins[1] += sc[1] * q
            return tuple(wins)


def p2(lines):
    p1 = int(lines[0].split(" ")[-1])
    p2 = int(lines[1].split(" ")[-1])

    return max(recurse(0, 0, p1, p2, True))


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()
    # print(p1(lines))
    print(p2(lines))
    # print(recurse.cache_info())
