#!/usr/bin/env python


def main():
    print(get_total(read_input()))


def get_total(values):
    return sum(x // 3 - 2 for x in values)


def read_input():
    with open("day1.txt") as f:
        return (int(x) for x in f.readlines())


if __name__ == "__main__":
    main()
