#! /usr/bin/env python3

import collections
import sys

from heapq import heapify, heappop, heappush
from pprint import pprint


COST = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

DST = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}


def print_pods(pods):
    print("#" * 13)

    line1 = ""
    for x in range(11):
        line1 += pods.get((x, 0), ".")
    print(line1.join("##"))

    line2 = ""
    for x in range(11):
        if x in range(2, 10, 2):
            delim = "."
        else:
            delim = "#"
        line2 += pods.get((x, 1), delim)
    print(line2.join("##"))

    line3 = ""
    for x in range(11):
        if x in range(2, 10, 2):
            delim = "."
        elif x < 1 or x > 9:
            delim = " "
        else:
            delim = "#"
        line3 += pods.get((x, 2), delim)
    print(line3.join("  "))

    line4 = "#" * 9
    print(line4.join("  ").join("  "))


def dbg_path(graph, path):
    n_graph = graph.copy()
    print_pods(n_graph)

    for src, dst in path:
        pod = n_graph[src]
        del n_graph[src]
        n_graph[dst] = pod

        print("----")
        print_pods(n_graph)
        print("----")


def parse_rooms_tuple(lines) -> list[tuple[str, tuple[int, int]]]:
    positions = {}
    for y in [2, 3]:
        for x, v in enumerate(lines[y][1:-1]):
            if v not in "#. ":
                positions[(x, y - 1)] = v

    return positions


def possible_moves(pods):

    def all_adjacent(point):
        if point[1] == 2:
            if (point[0], 1) in pods:
                return

        for itr in [
            # check left
            range(point[0], -1, -1),
            # check right
            range(point[0], 11),
        ]:
            for x in itr:
                if (x, 0) != point and (x, 0) in pods:
                    break

                # check rooms
                if x in range(2, 10, 2):
                    if point[0] != x and DST[pods[point]] == x and (x, 1) not in pods:
                        if (x, 2) not in pods:
                            yield (abs(point[0] - x) + point[1] + 2, (x, 2))
                        else:
                            yield (abs(point[0] - x) + point[1] + 1, (x, 1))

                # check hallway
                else:
                    yield (abs(point[0] - x) + point[1], (x, 0))

    for pos, pod in pods.items():
        if DST[pod] == pos[0]:
            # don't re-check pods that are where they're supposed to be
            if pos[1] == 2:
                continue

            if pos[1] == 1 and pods[(pos[0], 2)] == pod:
                continue

        for cost, dst in all_adjacent(pos):
            yield (cost * COST[pod], pod, dst, pos)


def hashed(d):
    # "hash" dict d into a tuple( list of d items ) to make it easier to check?
    return tuple(sorted(d.items()))


def p1(lines):
    graph = parse_rooms_tuple(lines)

    # print_pods(graph)

    # int -> hashed(graph)
    # keep track of cost it took to get to a particular state (but not the moves?)
    costs = {}

    # bfs
    queue = []

    h_d = hashed(graph)
    costs[h_d] = (0, [])
    heappush(queue, (0, h_d, []))

    win_state = hashed({
        tup: pod
        for pod, home in DST.items()
        for tup in [(home, 1), (home, 2)]
    })

    while queue:
        score, h_graph, path = heappop(queue)

        if h_graph == win_state:
            continue

        for cost, pod, dst, src in possible_moves(dict(h_graph)):
            ng = dict(h_graph)
            del ng[src]
            ng[dst] = pod
            h_ng = hashed(ng)
            n_path = path + [(src, dst)]
            if h_ng not in costs:
                # calc
                heappush(queue, (score + cost, h_ng, n_path))
                costs[h_ng] = (score + cost, n_path)
            elif h_graph in costs:
                # re calc
                n_score = costs[h_graph][0] + cost
                if n_score < costs[h_ng][0] or costs[h_ng][0] == 0:
                    costs[h_ng] = (n_score, n_path)  # todo make this tuple right
                    heappush(queue, (n_score, h_ng, n_path))

    score, path = costs[win_state]
    # dbg_path(graph, path)
    return score


def p2(lines):
    pass


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()

    print(p1(lines))
    # print(p2(lines))
