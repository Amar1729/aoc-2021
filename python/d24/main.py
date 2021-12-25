#! /usr/bin/env python3

"""
alu = ALU(lines)

# to figure out the problem -
for x, a in alu.alus:
    with open(f"alu{x}.txt", "w") as f:
        f.write("\n".join(a))

# then, from shell:
# for f in alu{[1-9],11,12,13}.txt; do diff alu0.txt $f; done
# ^ helps reveal some interesting things about each section of the input

for a in alu.alus:
    print(a[4], a[5], a[-3])

# here you can manually pair up and figure out constraints
for idx, a in enumerate(alu.alus):
    d = int(a[4].split()[-1])
    check = abs(int(a[5].split()[-1]))
    offset = int(a[-3].split()[-1])
    op = "+" if d == 1 else "-"
    print(f"{idx}: {op}{check if d == 26 else offset}")
"""


import functools
import re
import sys

try:
    assert sys.version_info.minor >= 10
except AssertionError:
    print(sys.version_info)
    raise


def run_alu(input_string: list[str], lines: list[str], target_d: dict[str, int]=None) -> int:
    d = target_d if target_d else {v: 0 for v in "wxyz"}

    digits = [int(c) for c in input_string]

    for line in lines:
        match line.split():
            case ["inp", ("w" | "x" | "y" | "z") as target]:
                # print(f"input received. d: {d}")
                # instrumented for automation
                # value = input(f"{target}: ")
                value = digits.pop(0)
                d[target] = int(value)

            case ["add", target, reg] if reg in "wxyz":
                d[target] += d[reg]
            case ["add", target, value] if re.match(r"\-?[0-9]", value):
                d[target] += int(value)

            case ["mul", target, reg] if reg in "wxyz":
                d[target] *= d[reg]
            case ["mul", target, value] if re.match(r"\-?[0-9]", value):
                d[target] *= int(value)

            case ["div", target, reg] if reg in "wxyz":
                d[target] //= d[reg]
            case ["div", target, value] if re.match(r"\-?[0-9]", value):
                d[target] //= int(value)

            case ["mod", target, reg] if reg in "wxyz":
                d[target] %= d[reg]
            case ["mod", target, value] if re.match(r"\-?[0-9]", value):
                d[target] %= int(value)

            case ["eql", target, reg] if reg in "wxyz":
                d[target] = int(d[target] == d[reg])
            case ["eql", target, value] if re.match(r"\-?[0-9]", value):
                d[target] = int(d[target] == int(reg))

    assert len(digits) == 0
    return d


class ALU:
    def __init__(self, lines):
        self.lines = lines
        content = "\n".join(lines)
        self.alus = [
            ["inp w"] + line.splitlines()
            for line in content.split("inp w\n") if line.strip()
        ]

    def execute(self, input_string: str) -> dict[str, int]:
        return run_alu(input_string, self.lines)

    @functools.cache
    def cached_execute(
            self,
            index: int = 0,
            w: int = 0,
            x: int = 0,
            y: int = 0,
            z: int = 0,
    ) -> dict[str, int]:
        d = {
            "w": w,
            "x": x,
            "y": y,
            "z": z,
        }
        return run_alu(str(w), self.alus[index], d)


def p1(lines: list[str]) -> int:
    soln = "39494195799979"

    # verify
    alu = ALU(lines)
    d = alu.execute(soln)
    assert d['z'] == 0

    return int(soln)


def p2(lines: list[str]) -> int:
    soln = "13161151139617"

    # verify
    alu = ALU(lines)
    d = alu.execute(soln)
    assert d['z'] == 0

    return int(soln)


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()
    print(p1(lines))
    print(p2(lines))
