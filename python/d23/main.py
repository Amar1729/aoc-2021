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

    for y in range(2, 5):
        if (y == 2) or (y > 2 and len(pods) > 8):
            line3 = ""
            for x in range(11):
                if x in range(2, 10, 2):
                    delim = "."
                elif x < 1 or x > 9:
                    delim = " "
                else:
                    delim = "#"
                line3 += pods.get((x, y), delim)
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


def parse_rooms_tuple(lines, p2=False) -> list[tuple[str, tuple[int, int]]]:
    positions = {}
    for y in [2, 3]:
        for x, v in enumerate(lines[y][1:-1]):
            if v not in "#. ":
                positions[(x, 4 if p2 and y == 3 else (y - 1))] = v

    # hard-coded extra input for part 2
    if p2:
        positions[(2, 2)] = "D"
        positions[(2, 3)] = "D"

        positions[(4, 2)] = "C"
        positions[(4, 3)] = "B"

        positions[(6, 2)] = "B"
        positions[(6, 3)] = "A"

        positions[(8, 2)] = "A"
        positions[(8, 3)] = "C"

    return positions


def possible_moves(pods, p2=False):

    def all_adjacent(point, p2=False):
        # check if we can actually get out this room (if we're in a room)
        if any((point[0], y) in pods for y in range(1, point[1])):
            return

        for itr in [
            # check left
            range(point[0] - 1, -1, -1),
            # check right
            range(point[0] + 1, 11),
        ]:
            for x in itr:
                if (x, 0) != point and (x, 0) in pods:
                    break

                # check rooms
                if point[0] != x and x in range(2, 10, 2):
                    pod = pods[point]
                    if DST[pod] == x:
                        max_y = 0
                        # this loop works because:
                        # 1) if any pod other than what's allowed in this room
                        # is present, it will be found an break the loop
                        # 2) if the non-full room has only pods allowed in it,
                        # then the spaces above them will be empty
                        # 3) if the room is full then no pods will pass the above
                        # DST[pod] == x check
                        for cy in range(4 if p2 else 2, 0, -1):
                            if (x, cy) in pods:
                                if pods[(x, cy)] != pod:
                                    max_y = -1
                                    break
                            else:
                                max_y = cy
                                break

                        if max_y > 0:
                            yield (abs(point[0] - x) + point[1] + max_y, (x, max_y))

                # check hallway
                else:
                    # can only move into hallway if we were in a room first
                    if point[1] > 0:
                        yield (abs(point[0] - x) + point[1], (x, 0))

    def column_required_move(point: tuple[int, int], p2: bool) -> bool:
        # check whether a given pod point needs to move out of its column
        # does not need to if it's at the bottom/above others of its type
        # in its destination column (does need to otherwise)
        pod = pods[point]
        y = point[1]

        # need to move if not in the right room
        if DST[pod] != point[0]:
            return True

        # if we're in destination room at maximum column value we're good
        if (p2 and y == 4) or (not p2 and y == 2):
            return False

        # check if there's anything not of this room below this pod
        below = range(y + 1, 5) if p2 else range(y + 1, 3)
        below_points = map(lambda iy: (point[0], iy), below)
        if any(p in pods and pods[p] != pod for p in below_points):
            return True

        # no move required!
        return False

    for pos, pod in pods.items():
        if column_required_move(pos, p2):
            for cost, dst in all_adjacent(pos, p2):
                yield (cost * COST[pod], pod, dst, pos)


def hashed(d):
    # "hash" dict d into a tuple( list of d items ) to make it easier to check?
    return tuple(sorted(d.items()))


def p1(lines, p2=False):
    graph = parse_rooms_tuple(lines, p2)

    # print_pods(graph)

    # int -> hashed(graph)
    # keep track of cost it took to get to a particular state
    costs = {}

    # bfs (stores an array of the moves as well for debugging)
    queue = []

    h_d = hashed(graph)
    costs[h_d] = (0, [])
    heappush(queue, (0, h_d, []))

    if p2:
        rows = range(1, 5)
    else:
        rows = range(1, 3)

    win_state = hashed({
        tup: pod
        for pod, home in DST.items()
        for tup in [(home, y) for y in rows]
    })

    while queue:
        score, h_graph, path = heappop(queue)

        if h_graph == win_state:
            continue

        for cost, pod, dst, src in possible_moves(dict(h_graph), p2):
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
                    costs[h_ng] = (n_score, n_path)
                    heappush(queue, (n_score, h_ng, n_path))

    score, path = costs[win_state]
    # dbg_path(graph, path)
    return score


def p2(lines):
    return p1(lines, True)


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()

    # print(p1(lines))
    print(p2(lines))
