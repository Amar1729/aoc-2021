#! /usr/bin/env python3

# 5438
# 6301: too high
# 5788: too high
# 5401

import sys


def print_grid(grid):
    points_x = sorted([int(k.real) for k in grid])
    min_x = points_x[0]
    max_x = points_x[-1]

    points_y = sorted([int(k.imag) for k in grid])
    min_y = points_y[0]
    max_y = points_y[-1]

    for j in range(min_y, max_y + 1):
        for i in range(min_x, max_x + 1):
            if complex(i, j) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()


def dbg(grid):
    points_x = sorted([int(k.real) for k in grid])
    min_x = points_x[0]
    max_x = points_x[-1]

    points_y = sorted([int(k.imag) for k in grid])
    min_y = points_y[0]
    max_y = points_y[-1]

    print("size of grid: ", min_x, max_x, min_y, max_y)
    print_grid(grid)


def get_surrounding(x: int, y: int, grid: set[complex], default_pixel: str) -> int:
    if default_pixel == ".":
        non_default_value = "1"
        default_value = "0"
    else:
        non_default_value = "0"
        default_value = "1"

    surrounding = ""
    for j in [-1, 0, 1]:
        for i in [-1, 0, 1]:
            surrounding += non_default_value if complex(x + i, y + j) in grid else default_value

    return int(surrounding, 2)


def complement_grid(grid):
    # flip a grid from '#' to '.'
    points_x = sorted([int(k.real) for k in grid])
    min_x = points_x[0]
    max_x = points_x[-1]

    points_y = sorted([int(k.imag) for k in grid])
    min_y = points_y[0]
    max_y = points_y[-1]

    new_grid = set()
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if complex(x, y) not in grid:
                new_grid.add(complex(x, y))

    return new_grid


def step(grid: set[complex], transform: str) -> set[complex]:
    # also have to track the possible pixel values that the pixels at infinity
    # might transform to (. -> # is possible if transform[0] == '#', etc)
    start_pixel = transform[0]
    end_pixel = transform[-1]

    # assume pixels at infinity are dark
    default_pixel = "."
    # default_pixel = "#" if start_pixel == "." else "."

    # print_grid(grid)
    print("size of input: ", len(lines[2]), len(lines[2:]))
    print()

    points_x = sorted([int(k.real) for k in grid])
    points_y = sorted([int(k.imag) for k in grid])
    rx = range(points_x[0] - 1, points_x[-1] + 2)
    ry = range(points_y[0] - 1, points_y[-1] + 2)

    new_grid = set()
    for y in ry:
        for x in rx:
            # new_pixel = transform[get_surrounding(x, y)]
            new_pixel = transform[get_surrounding(x, y, grid, default_pixel)]
            # print(x, y, ": ", ("#" if complex(x, y) in grid else "."), new_pixel)
            if new_pixel != default_pixel:
                new_grid.add(complex(x, y))

    if default_pixel == "#":
        dbg(complement_grid(new_grid))
    else:
        dbg(new_grid)
    # print_grid(new_grid)
    print()

    if default_pixel == ".":
        if start_pixel == "#":
            default_pixel = "#"

    # if default_pixel == "#":
    else:
        if end_pixel == ".":
            default_pixel = "."

    return new_grid


def p1(lines):
    transform = lines[0]

    grid = {
        complex(i, j)
        for j, row in enumerate(lines[2:])
        for i, value in enumerate(row)
        if value == "#"
    }

    for _ in range(2):
        grid = step(grid, transform)

    return len(grid)


def p2(lines):
    pass


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()

    print(p1(lines))
    # print(p2(lines))
