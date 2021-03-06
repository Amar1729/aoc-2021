#! /usr/bin/env python3

import sys


class Board:
    def __init__(self, grid):
        self.grid = grid
        self.marked = [[0 for _ in range(5)] for _ in range(5)]

        self.total = sum(sum(row) for row in self.grid)

    def mark(self, number) -> bool:
        for x, row in enumerate(self.grid):

            if number in row:
                mark = row.index(number)
                self.marked[x][mark] = 1

                self.total -= number
                self.prev = number
                return True

        return False

    def complete(self) -> bool:
        if any(sum(row) == 5 for row in self.marked):
            return True

        if any(sum(col) == 5 for col in zip(*self.marked)):
            return True

        return False

    def score(self) -> int:
        return self.total * self.prev


def parse(lines):
    numbers = list(map(int, lines[0].split(',')))
    lines.pop(0)
    lines.pop(0)

    boards = []
    grid = []
    while lines:
        if lines[0]:
            grid.append(list(map(int, lines.pop(0).split())))
        else:
            boards.append(Board(grid))
            grid = []
            lines.pop(0)

    if grid:
        boards.append(Board(grid))

    return numbers, boards


def p1(lines):
    numbers, boards = parse(lines)

    for n in numbers:
        for b in boards:
            b.mark(n)

            if b.complete():
                return b.score()


def p2(lines):
    numbers, boards = parse(lines)

    for n in numbers:
        completed = []
        for b_idx in range(len(boards)):
            boards[b_idx].mark(n)
            if boards[b_idx].complete():
                completed.append(b_idx)

        if len(boards) == 1 and boards[0].complete():
            return boards[0].score()

        for b_idx in completed[::-1]:
            boards.pop(b_idx)

    print(boards)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
