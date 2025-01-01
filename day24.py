#!/usr/bin/env python
INITIAL = """\
....#
#..#.
#..##
..#..
#...."""


def string_to_board(initial):
    board = {}
    for y, line in enumerate(initial.split("\n")):
        line = line.strip()
        for x, value in enumerate(line.strip()):
            # Use (y,x) so that we can use divmod easily in biodiversity function
            board[(y, x)] = 1 if value == "#" else 0
    return board


def biodiversity(board):
    return sum(board[divmod(i, 5)] << i for i in range(25))


def read_input(filename):
    with open(filename) as f:
        return f.read()


def neigbours(point):
    x, y = point
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        yield x + dx, y + dy


def new_board(board):
    new_board = {}
    for k, v in board.items():
        num_adjacent = sum(board.get(n, 0) for n in neigbours(k))
        if v:
            v = num_adjacent == 1
        else:
            v = num_adjacent in (1, 2)
        new_board[k] = int(v)
    return new_board


def print_board(board):
    for y in range(5):
        print("".join(str(board[y, x]) for x in range(5)))
    print()


def main():
    board = string_to_board(read_input("day24.txt"))
    seen = set()

    while True:
        score = biodiversity(board)
        if score in seen:
            break
        seen.add(score)
        board = new_board(board)

    return score


if __name__ == "__main__":
    score = main()
    print(score)
