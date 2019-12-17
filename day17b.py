#!/usr/bin/env python

# FIXME can we avoid having globals?
INPUT_VALUES = []
OUTPUT_VALUES = []

relative_base = 0


def is_intersection(positions, point):
    x, y = point
    neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return all(x in positions for x in neighbours)


def main():
    values = read_input()

    position = 0
    while position != -1:
        position = do_turn(values, position)

    ascii_values = "".join(chr(x) for x in OUTPUT_VALUES)
    lines = [list(line) for line in ascii_values.split("\n")]

    # print the maze
    for line in ascii_values.split("\n"):
        print("".join(line))

    positions = set()
    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            if val == "#":
                positions.add((x, y))
            elif val == "^":
                positions.add((x, y))
                robot = (x, y)

    intersections = [p for p in positions if is_intersection(positions, p)]

    moves = solve_maze(positions, robot, direction="U")
    main_routine, func_a, func_b, func_c = split_moves(moves)
    video_feed = "n"

    instructions = sum(
        (
            ascii_instructions(x)
            for x in (main_routine, func_a, func_b, func_c, video_feed)
        ),
        [],
    )
    # Drop existing output before re-running program
    while OUTPUT_VALUES:
        OUTPUT_VALUES.pop()

    INPUT_VALUES.extend(instructions)
    # re-read initial intcode program
    values = read_input()
    # Force robot to wake up
    assert values[0] == 1
    values[0] = 2
    position = 0
    while position != -1:
        position = do_turn(values, position)

    # I was expecting a single output but actually list is 4769 elements long
    # Therefore return the final element
    # print(len(OUTPUT_VALUES))
    return OUTPUT_VALUES[-1]


def ascii_instructions(instructions):
    return [ord(x) for x in instructions + "\n"]


def split_moves(moves):
    func_a = "R,6,L,10,R,10,R,10"
    func_b = "L,10,L,12,R,10"
    func_c = "R,6,L,12,L,10"
    main_routine = moves.replace(func_a, "A").replace(func_b, "B").replace(func_c, "C")
    return (main_routine, func_a, func_b, func_c)


move = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}

turn_right = {"U": "R", "R": "D", "D": "L", "L": "U"}

turn_left = {"U": "L", "R": "U", "D": "R", "L": "D"}


def forward(robot, direction):
    x, y = robot
    dx, dy = move[direction]
    return x + dx, y + dy


def solve_maze(positions, robot, direction):
    output = []

    while True:
        distance = 0
        while forward(robot, direction) in positions:
            robot = forward(robot, direction)
            distance += 1

        if distance:
            output.append(distance)

        if forward(robot, turn_right[direction]) in positions:
            direction = turn_right[direction]
            output.append("R")
        elif forward(robot, turn_left[direction]) in positions:
            direction = turn_left[direction]
            output.append("L")
        else:
            return ",".join(str(x) for x in output)


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
    with open("day17.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    dust = main()
    print("Dust: %s" % dust)
