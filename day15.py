#!/usr/bin/env python
import random

# FIXME can we avoid having globals?
INPUT_VALUES = []
OUTPUT_VALUES = []

relative_base = 0

move = {1: (0, 1), 4: (1, 0), 2: (0, -1), 3: (-1, 0)}  # North  # East  # South  # West

reverse_move = {1: 2, 2: 1, 3: 4, 4: 3}


def next_move(map, position, previous_moves=None):
    moves = list(range(1, 5))
    random.shuffle(moves)
    for move in moves:
        new_pos = new_position(position, move)
        if new_pos not in map:
            # Try to move somewhere we haven't gone before
            return move
    else:
        if previous_moves:
            # backtrack
            return reverse_move[previous_moves.pop()]


def new_position(position, direction):
    x, y = position
    dx, dy = move[direction]
    return (x + dx, y + dy)


def main():
    values = read_input()
    robot_position = (0, 0)
    previous_moves = []
    map = {}
    map[robot_position] = 1
    move = next_move(map, robot_position)
    INPUT_VALUES.append(move)
    position = 0
    while position != -1:
        position = do_turn(values, position)
        if OUTPUT_VALUES:
            output = OUTPUT_VALUES.pop()
            new = new_position(robot_position, move)
            if output in (1, 2):
                robot_position = new
                if new not in map:
                    previous_moves.append(move)
                if output == 2:
                    # How many moves did it take to get here
                    # Note that if there were multiple branches that get here,
                    # then this might not be the shortest path
                    print("Length: %s" % len(previous_moves))
            map[new] = output
            move = next_move(map, robot_position, previous_moves)
            INPUT_VALUES.append(move)

    print_map(map)


char = {0: "█", 1: " ", 2: "X", None: "?"}


def print_map(map):
    max_x = max(x for x, y in map.keys())
    min_x = min(x for x, y in map.keys())
    max_y = max(y for x, y in map.keys())
    min_y = min(y for x, y in map.keys())
    for y in range(max_y, min_y - 1, -1):
        line = "".join(char[map.get((x, y))] for x in range(min_x, max_x + 1))
        print(line)


def extend_if_required(values, pos):
    if pos + 1 > len(values):
        values.extend([0] * (pos + 1 - len(values)))


def get_pos(values, mode, position):
    if mode == 1:
        pos = position
    elif mode == 0:
        pos = values[position]
    elif mode == 2:
        pos = relative_base + values[position]

    extend_if_required(values, pos)
    return pos


def do_add(values, modes, start_position):
    pos_a = get_pos(values, modes[0], start_position + 1)
    pos_b = get_pos(values, modes[1], start_position + 2)
    pos_destination = get_pos(values, modes[2], start_position + 3)

    values[pos_destination] = values[pos_a] + values[pos_b]
    return start_position + 4


def do_multiply(values, modes, start_position):
    pos_a = get_pos(values, modes[0], start_position + 1)
    pos_b = get_pos(values, modes[1], start_position + 2)
    pos_destination = get_pos(values, modes[2], start_position + 3)

    values[pos_destination] = values[pos_a] * values[pos_b]
    return start_position + 4


def do_input(values, modes, start_position):
    # should always be in position mode
    assert modes[0] != 1
    pos_destination = get_pos(values, modes[0], start_position + 1)

    values[pos_destination] = INPUT_VALUES.pop(0)
    return start_position + 2


def do_output(values, modes, start_position):
    pos_a = get_pos(values, modes[0], start_position + 1)

    output = values[pos_a]
    OUTPUT_VALUES.append(output)
    return start_position + 2


def do_jump_if_true(values, modes, start_position):
    pos_a = get_pos(values, modes[0], start_position + 1)
    pos_b = get_pos(values, modes[1], start_position + 2)

    if values[pos_a]:
        return values[pos_b]
    else:
        return start_position + 3


def do_jump_if_false(values, modes, start_position):
    pos_a = get_pos(values, modes[0], start_position + 1)
    pos_b = get_pos(values, modes[1], start_position + 2)

    if not values[pos_a]:
        return values[pos_b]
    else:
        return start_position + 3


def do_less_than(values, modes, start_position):
    pos_a = get_pos(values, modes[0], start_position + 1)
    pos_b = get_pos(values, modes[1], start_position + 2)
    pos_destination = get_pos(values, modes[2], start_position + 3)

    new_value = 1 if values[pos_a] < values[pos_b] else 0
    values[pos_destination] = new_value
    return start_position + 4


def do_equals(values, modes, start_position):
    pos_a = get_pos(values, modes[0], start_position + 1)
    pos_b = get_pos(values, modes[1], start_position + 2)
    pos_destination = get_pos(values, modes[2], start_position + 3)

    new_value = 1 if values[pos_a] == values[pos_b] else 0
    values[pos_destination] = new_value
    return start_position + 4


def do_relative_base(values, modes, start_position):
    global relative_base
    pos_a = get_pos(values, modes[0], start_position + 1)
    relative_base += values[pos_a]
    return start_position + 2


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
    elif opcode == 9:
        position = do_relative_base(values, modes, start_position)
    else:
        raise ValueError("Unexpected opcode: %s", opcode)

    return position


def read_input():
    with open("day15.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    main()
