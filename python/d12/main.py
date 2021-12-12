#! /usr/bin/env python3

import copy
import sys
import collections
import itertools
import functools
import math

from pprint import pprint


def dfs(path, node, graph):
    paths = []
    for n in graph[node]:
        if n == "end":
            paths.append(path + ["end"])
        elif n == "start":
            pass
        else:
            # if n not in path:
            if n.upper() == n or n not in path:
                paths.extend(dfs(path + [n], n, graph))

    return paths


def p1(lines):
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

    return len(list(dfs(["start"], "start", graph)))


def p2(lines):
    pass


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    print(p1(lines))
    # print(p2(lines))
