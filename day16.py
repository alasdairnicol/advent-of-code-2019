#!/usr/bin/env python
import itertools

BASE_SIGNAL = [0, 1, 0, -1]


def get_input_signal(filename):
    with open(filename) as f:
        return [int(x) for x in f.read().strip()]


def get_multipliers(r):
    for digit in itertools.cycle(BASE_SIGNAL):
        for _ in range(r):
            yield digit


def do_phase(input_signal):
    return [do_round(input_signal, x) for x in range(1, len(input_signal) + 1)]


def do_round(input_signal, r):
    multipliers = get_multipliers(r)
    next(multipliers)  # discard the first item
    return abs(sum(x * y for x, y in zip(input_signal, multipliers))) % 10


def main():
    input_signal = get_input_signal("day16.txt")
    for phase in range(100):
        input_signal = do_phase(input_signal)
    return int("".join(str(x) for x in input_signal[:8]))


if __name__ == "__main__":
    signal = main()
    print(signal)
