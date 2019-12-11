#!/usr/bin/env python

# FIXME can we avoid having globals?
INPUT_VALUES = []
OUTPUT_VALUES = []

relative_base = 0

turn_right = {
    "U": "R",
    "R": "D",
    "D": "L",
    "L": "U",
}

turn_left = {
    "U": "L",
    "R": "U",
    "D": "R",
    "L": "D",
}

move = {
    "U": (0, 1),
    "R": (1, 0),
    "D": (0, -1),
    "L": (-1, 0),
}


def main():
    values = read_input()
    robot_position = (0, 0)
    robot_direction = "U"
    panels = {}
    paint = True

    INPUT_VALUES.append(panels.get(robot_position, 0))

    position = 0
    while position != -1:
        position = do_turn(values, position)

        if OUTPUT_VALUES:
            output = OUTPUT_VALUES.pop()
            if paint:
                panels[robot_position] = output
            else:
                if output == 0:
                    robot_direction = turn_left[robot_direction]
                else:
                    robot_direction = turn_right[robot_direction]
                next_move = move[robot_direction]
                robot_position = (
                    robot_position[0] + next_move[0],
                    robot_position[1] + next_move[1],
                )
                INPUT_VALUES.append(panels.get(robot_position, 0))
            paint = not (paint)

    return len(panels)


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
    with open("day11.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    num_panels = main()
    print(num_panels)
