#!/usr/bin/env python
import itertools


def main():
    values = read_input()
    max_seen = 0
    max_permutation = None
    for permutation in itertools.permutations(range(5, 10)):
        output = try_phase_settings(values, permutation)
        if output > max_seen:
            max_seen = output
            max_permutation = permutation

    return max_permutation, max_seen


def try_phase_settings(values, phase_settings):
    amplifiers = [values.copy() for _ in range(5)]
    positions = [0] * 5
    inputs = [[phase] for phase in phase_settings]
    inputs[0] += [0]
    running = [True] * 5

    while True in running:
        for x in range(5):
            if running[x]:
                output, position = do_turn(amplifiers[x], inputs[x], positions[x])
                if position == -1:
                    running[x] = False
                else:
                    positions[x] = position
                if output is not None:
                    inputs[(x + 1) % 5].append(output)

    return inputs[0][0]


def do_add(values, modes, start_position):
    if modes[0]:
        pos_a = start_position + 1
    else:
        pos_a = values[start_position + 1]

    if modes[1]:
        pos_b = start_position + 2
    else:
        pos_b = values[start_position + 2]

    if modes[2]:
        pos_destination = start_position + 3
    else:
        pos_destination = values[start_position + 3]

    values[pos_destination] = values[pos_a] + values[pos_b]
    return start_position + 4


def do_multiply(values, modes, start_position):
    if modes[0]:
        pos_a = start_position + 1
    else:
        pos_a = values[start_position + 1]

    if modes[1]:
        pos_b = start_position + 2
    else:
        pos_b = values[start_position + 2]

    if modes[2]:
        pos_destination = start_position + 3
    else:
        pos_destination = values[start_position + 3]

    values[pos_destination] = values[pos_a] * values[pos_b]
    return start_position + 4


def do_input(values, modes, start_position, inputs):
    # should always be in position mode
    assert not modes[0]

    # No-op if there are not any inputs yet
    if not inputs:
        return start_position

    pos_destination = values[start_position + 1]

    values[pos_destination] = inputs.pop(0)
    return start_position + 2


def do_output(values, modes, start_position):
    if modes[0]:
        pos_a = start_position + 1
    else:
        pos_a = values[start_position + 1]

    output = values[pos_a]
    return output, start_position + 2


def do_jump_if_true(values, modes, start_position):
    if modes[0]:
        pos_a = start_position + 1
    else:
        pos_a = values[start_position + 1]

    if modes[1]:
        pos_b = start_position + 2
    else:
        pos_b = values[start_position + 2]

    if values[pos_a]:
        return values[pos_b]
    else:
        return start_position + 3


def do_jump_if_false(values, modes, start_position):
    if modes[0]:
        pos_a = start_position + 1
    else:
        pos_a = values[start_position + 1]

    if modes[1]:
        pos_b = start_position + 2
    else:
        pos_b = values[start_position + 2]

    if not values[pos_a]:
        return values[pos_b]
    else:
        return start_position + 3


def do_less_than(values, modes, start_position):
    if modes[0]:
        pos_a = start_position + 1
    else:
        pos_a = values[start_position + 1]

    if modes[1]:
        pos_b = start_position + 2
    else:
        pos_b = values[start_position + 2]

    if modes[2]:
        pos_destination = start_position + 3
    else:
        pos_destination = values[start_position + 3]

    new_value = 1 if values[pos_a] < values[pos_b] else 0
    values[pos_destination] = new_value
    return start_position + 4


def do_equals(values, modes, start_position):
    if modes[0]:
        pos_a = start_position + 1
    else:
        pos_a = values[start_position + 1]

    if modes[1]:
        pos_b = start_position + 2
    else:
        pos_b = values[start_position + 2]

    if modes[2]:
        pos_destination = start_position + 3
    else:
        pos_destination = values[start_position + 3]

    new_value = 1 if values[pos_a] == values[pos_b] else 0
    values[pos_destination] = new_value
    return start_position + 4


def get_modes(instruction):
    zero_padded = "%05d" % instruction
    return [int(x) for x in zero_padded[-3::-1]]


def do_turn(values, inputs, start_position):
    instruction = values[start_position]
    opcode = instruction % 100
    modes = get_modes(instruction)
    output = None

    if opcode == 99:
        return output, -1

    if opcode == 1:
        position = do_add(values, modes, start_position)
    elif opcode == 2:
        position = do_multiply(values, modes, start_position)
    elif opcode == 3:
        position = do_input(values, modes, start_position, inputs)
    elif opcode == 4:
        output, position = do_output(values, modes, start_position)
    elif opcode == 5:
        position = do_jump_if_true(values, modes, start_position)
    elif opcode == 6:
        position = do_jump_if_false(values, modes, start_position)
    elif opcode == 7:
        position = do_less_than(values, modes, start_position)
    elif opcode == 8:
        position = do_equals(values, modes, start_position)
    else:
        raise ValueError("Unexpected opcode: %s", opcode)

    return output, position


def read_input():
    with open("day7.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    max_permutation, max_seen = main()
    print("Max seen %s for %s" % (max_seen, ",".join(str(x) for x in max_permutation)))
