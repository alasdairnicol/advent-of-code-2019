#!/usr/bin/env python


def get_fuel(x):
    fuel = x // 3 - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + get_fuel(fuel)


def main():
    print(get_total(read_input()))


def get_total(values):
    return sum(get_fuel(x) for x in values)


def read_input():
    with open("day01.txt") as f:
        return (int(x) for x in f.readlines())


if __name__ == "__main__":
    main()
