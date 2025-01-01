#!/usr/bin/env python
import itertools
import functools

BASE_SIGNAL = [0, 1, 0, -1]


def get_input_signal(filename):
    with open(filename) as f:
        return [int(x) for x in f.read().strip()]


def get_multipliers(r):
    for digit in itertools.cycle(BASE_SIGNAL):
        for _ in range(r):
            yield digit


def do_phase(input_signal):
    """
    For input signal t u v w x y z

    itertools.accumuate() lets us generate

    z, z+y, z+y+x, z+y+x+w, ... (all mod 10)

    We then reverse the list to get the output signal
    """
    return list(
        itertools.accumulate(reversed(input_signal), func=lambda x, y: (x + y) % 10)
    )[::-1]


def do_round(input_signal, r):
    multipliers = get_multipliers(r)
    next(multipliers)  # discard the first item
    out_list = (x * y for x, y in zip(input_signal, multipliers))
    out = functools.reduce(lambda x, y: (x + y) % 10, out_list)
    if out < 0:
        out += 10
    return out


def main():
    input_signal = get_input_signal("day16.txt")

    # input_signal = [int(x) for x in "03036732577212944063491565474664"]
    input_signal = input_signal * 10000
    offset = int("".join(str(x) for x in input_signal[:7]))

    # Once we are more than half way through the list, the output for
    # the nth digit is nth + (n+1)th + (n+2)th digits. It does not
    # depend on 0 - (n-1)th digits, so we can discard them.
    assert offset > len(input_signal) / 2

    input_signal = input_signal[offset:]

    for phase in range(100):
        input_signal = do_phase(input_signal)
    return int("".join(str(x) for x in input_signal[:8]))


if __name__ == "__main__":
    signal = main()
    print(signal)
