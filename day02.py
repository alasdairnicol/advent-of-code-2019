#!/usr/bin/env python


def main():
    start_position = 0
    values = read_input()
    values[1:3] = (12, 2)
    while start_position != -1:
        start_position = do_turn(values, start_position)

    print(values[0])


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
    with open("day02.txt") as f:
        return [int(x) for x in f.read().split(",")]


if __name__ == "__main__":
    main()
