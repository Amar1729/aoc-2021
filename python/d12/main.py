#! /usr/bin/env python3

import copy
import sys
import collections
import itertools
import functools
import math

from pprint import pprint


def check_path(path):
    lowers = set()
    for n in path:
        if n in lowers:
            return False
        if n not in ["start", "end"] and n.lower() == n:
            lowers.add(n)

    return True


def dfs(path, node, graph, p2):
    paths = []
    for n in graph[node]:
        if n == "end":
            paths.append(path + ["end"])
        elif n == "start":
            pass
        else:
            if n.upper() == n or n not in path:
                paths.extend(dfs(path + [n], n, graph, p2))
            else:
                # lowercase, possible duplicates
                # make sure no other twos
                if p2 and check_path(path):
                    paths.extend(dfs(path + [n], n, graph, p2))

    return paths


def p1(lines, p2=False):
    graph = {}
    for edge in lines:
        begin, end = edge.split("-")
        if begin in graph:
            graph[begin].append(end)
        else:
            graph[begin] = [end]

        if end in graph:
            graph[end].append(begin)
        else:
            if end != "end":
                graph[end] = [begin]

    return len(list(dfs(["start"], "start", graph, p2)))


def p2(lines):
    return p1(lines, True)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
