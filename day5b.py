#!/usr/bin/env python

# FIXME can we avoid having globals?
INPUT_VALUES = [5]
OUTPUT_VALUES = []


def main():
    values = read_input()
    position = 0
    while position != -1:
        position = do_turn(values, position)


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


def do_input(values, modes, start_position):
    # should always be in position mode
    assert not modes[0]
    pos_destination = values[start_position + 1]

    values[pos_destination] = INPUT_VALUES.pop(0)
    return start_position + 2


def do_output(values, modes, start_position):
    if modes[0]:
        pos_a = start_position + 1
    else:
        pos_a = values[start_position + 1]

    output = values[pos_a]
    OUTPUT_VALUES.append(output)
    return start_position + 2


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

        
    new_value = 1 if values[pos_a]  < values[pos_b] else 0 
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


def do_turn(values, start_position):
    instruction = values[start_position]
    opcode = instruction % 100
    modes = get_modes(instruction)

    if opcode == 99:
        return -1

    if opcode == 1:
        position = do_add(values, modes, start_position)
    elif opcode == 2:
        position = do_multiply(values, modes, start_position)
    elif opcode == 3:
        position = do_input(values, modes, start_position)
    elif opcode == 4:
        position = do_output(values, modes, start_position)
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

    return position


def read_input():
    with open("day5.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    main()
    assert all(v == 0 for v in OUTPUT_VALUES[:-1])
    print(OUTPUT_VALUES[-1])
