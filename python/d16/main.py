#! /usr/bin/env python3

import sys
import collections
import itertools
import functools
import math

from pprint import pprint


def hex_to_bits(h: str) -> str:
    h_value = int(h, 16)
    b = bin(h_value)[2:]
    return f"{b:>04}"


class Packet:
    def __init__(self, length: int, version: int, type_id: int, stuff):
        self.length = length
        self.version = version
        self.type_id = type_id
        self.stuff = stuff

        # assumes packets wont be modified
        self.version_sum = version + (sum(p.version_sum for p in stuff) if isinstance(stuff, list) else 0)

    def value(self) -> int:
        if self.type_id == 4:
            return self.stuff
        elif self.type_id == 0:
            # sum
            return sum(p.value() for p in self.stuff)
        elif self.type_id == 1:
            # product
            return math.prod(p.value() for p in self.stuff)
        elif self.type_id == 2:
            # minimum
            return min(p.value() for p in self.stuff)
        elif self.type_id == 3:
            # maximum
            return max(p.value() for p in self.stuff)
        elif self.type_id == 5:
            # >
            return self.stuff[0].value() > self.stuff[1].value()
        elif self.type_id == 6:
            # <
            return self.stuff[0].value() < self.stuff[1].value()
        elif self.type_id == 7:
            # =
            return self.stuff[0].value() == self.stuff[1].value()

        raise TypeError

    def __str__(self):
        return "\n".join([
            str(self.length),
            str(self.version),
            str(self.type_id),
            str(self.stuff),
        ])


def parse_packet(s):
    old_len = len(s)

    version, s = int(s[:3], 2), s[3:]
    type_id, s = int(s[:3], 2), s[3:]

    if type_id == 4:
        curr = 6
        literals = []
        while True:
            if s[0] == "0":
                curr += 5
                literals.append(s[1:5])
                s = s[5:]
                break
            else:
                curr += 5
                literals.append(s[1:5])
                s = s[5:]

        # curr = 4 * math.ceil(curr / 4)
        # s = s[curr:]
        if curr < old_len:
            diff = old_len - curr
            if all(c == "0" for c in s[:diff]):
                curr = old_len
                s = s[diff:]

        value = int("".join(literals), 2)

        return Packet(curr, version, type_id, value), s

    # elif type_id == 6:
    else:
        length_type_id = s[0]
        s = s[1:]
        curr = 7

        if length_type_id == "0":
            curr += 15

            sub_packet_length = int(s[:15], 2)
            s = s[15:]

            packets = []

            sub_packets_parsed = 0
            while sub_packets_parsed < sub_packet_length:
                p, s = parse_packet(s)
                curr += p.length
                sub_packets_parsed += p.length
                packets.append(p)

            return Packet(curr, version, type_id, packets), s
        else:
            curr += 11

            num_subpackets = int(s[:11], 2)
            s = s[11:]

            packets = []
            for _ in range(num_subpackets):
                p, s = parse_packet(s)
                curr += p.length
                packets.append(p)

            return Packet(curr, version, type_id, packets), s

    raise TypeError


def p1(lines, p2=False):
    input_hex = lines[0]
    input_bin = "".join([
        hex_to_bits(h)
        for h in input_hex
    ])

    s = input_bin

    packets = []
    while s:
        p, s = parse_packet(s)
        packets.append(p)

    if p2:
        return packets[0].value()

    return sum(p.version_sum for p in packets)


def p2(lines):
    return p1(lines, True)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.readlines()]

    # print(p1(lines))
    print(p2(lines))
