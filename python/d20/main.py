#! /usr/bin/env python3

import sys


def get_surrounding(x: int, y: int, grid: dict[complex, str], default_pixel: str) -> int:
    surrounding = ""
    for j in [-1, 0, 1]:
        for i in [-1, 0, 1]:
            surrounding += grid.get(complex(x + i, y + j), default_pixel)

    surrounding = surrounding.replace(".", "0").replace("#", "1")
    return int(surrounding, 2)


def step(grid: dict[complex, str], transform: str, default_pixel) -> dict[complex, str]:
    points_x = sorted([int(k.real) for k in grid])
    points_y = sorted([int(k.imag) for k in grid])
    rx = range(points_x[0] - 1, points_x[-1] + 2)
    ry = range(points_y[0] - 1, points_y[-1] + 2)

    new_grid = {}
    for y in ry:
        for x in rx:
            new_pixel = transform[get_surrounding(x, y, grid, default_pixel)]
            new_grid[complex(x, y)] = new_pixel

    return new_grid


def p1(lines, steps=2):
    transform = lines[0]

    grid = {
        complex(i, j): value
        for j, row in enumerate(lines[2:])
        for i, value in enumerate(row)
    }

    for _ in range(steps // 2):
        default_pixel = "."
        grid = step(grid, transform, default_pixel=default_pixel)
        if transform[0] == "#" and transform[-1] == ".":
            default_pixel = "#"
        grid = step(grid, transform, default_pixel=default_pixel)

    return len(list(filter(lambda p: p == "#", grid.values())))


def p2(lines):
    # apparently, the unoptimized version (keeping track of all pixels =
    # instead of ~half) works fine for p2 (~3.5sec)
    return p1(lines, 50)


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()

    # print(p1(lines))
    print(p2(lines))
