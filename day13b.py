#!/usr/bin/env python

# FIXME can we avoid having globals?
INPUT_VALUES = [0]
OUTPUT_VALUES = []

relative_base = 0


def main():
    values = read_input()
    values[0] = 2
    tiles = {}

    ball = None
    paddle = None
    score = None

    position = 0
    while position != -1:
        if ball is None or paddle is None or ball[0] == paddle[0]:
            new_direction = 0
        elif ball[0] > paddle[0]:
            new_direction = 1
        elif ball[0] < paddle[0]:
            new_direction = -1
        if INPUT_VALUES:
            INPUT_VALUES.pop()
        INPUT_VALUES.append(new_direction)

        position = do_turn(values, position)
        if len(OUTPUT_VALUES) == 3:
            tile_id, y, x = (
                OUTPUT_VALUES.pop(),
                OUTPUT_VALUES.pop(),
                OUTPUT_VALUES.pop(),
            )
            if (x, y) == (-1, 0):
                score = tile_id
            tiles[(x, y)] = tile_id
            if tile_id == 3:
                paddle = (x, y)
            elif tile_id == 4:
                ball = (x, y)

    return score


tile_types = {
    0: " ",
    1: "|",
    2: "X",
    3: "_",
    4: "O",
}


def draw_tiles(tiles):
    lines = []
    min_x, max_x, min_y, max_y = get_bounds(tiles)
    for y in range(min_y, max_y):
        lines.append([tiles.get((x, y), 0) for x in range(min_x, max_x + 1)])
    for line in lines:
        print("".join(tile_types[l] for l in line))


def get_bounds(tiles):
    xs, ys = zip(*tiles)
    return min(xs), max(xs), min(ys), max(ys)


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
    with open("day13.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    score = main()
    print(f"Final score: {score}")
