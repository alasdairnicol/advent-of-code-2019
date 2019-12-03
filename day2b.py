#!/usr/bin/env python


def main():
    original_values = read_input()

    for x in range(0, 100):
        for y in range(0, 100):
            start_position = 0
            values = list(original_values)  # copy values
            values[1] = x
            values[2] = y

            while start_position != -1:
                start_position = do_turn(values, start_position)

            if values[0] == 19690720:
                return x, y


def do_turn(values, start_position):
    opcode = values[start_position]

    if opcode == 99:
        return -1

    a = values[start_position + 1]
    b = values[start_position + 2]
    destination = values[start_position + 3]

    if opcode == 1:
        values[destination] = values[a] + values[b]
    elif opcode == 2:
        values[destination] = values[a] * values[b]
    return start_position + 4


def read_input():
    with open("day2.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    x, y = main()
    print(100 * x + y)
