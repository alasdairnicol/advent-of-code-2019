INITIAL = """\
....#
#..#.
#..##
..#..
#...."""


def read_input(filename):
    with open(filename) as f:
        return f.read()


class Board:
    def __init__(self, boards, level):
        self.boards = boards
        self.level = level
        self.board = {}
        boards[level] = self

    def get_board(self, level):
        if level not in self.boards:
            self.boards[level] = Board(self.boards, level)
        return self.boards[level]

    @staticmethod
    def from_string(boards, initial):
        board = Board(boards, level=0)
        board.board = {}
        for y, line in enumerate(initial.split("\n")):
            line = line.strip()
            for x, value in enumerate(line.strip()):
                board.board[(x, y)] = 1 if value == "#" else 0
        return board

    def num_adjacent(self, point):
        count = 0
        x, y = point

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if new_x == new_y == 2:
                inner_board = self.get_board(self.level + 1)
                if dx == 1:
                    points = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
                elif dx == -1:
                    points = [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
                if dy == 1:
                    points = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
                elif dy == -1:
                    points = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
                for point in points:
                    count += inner_board.board.get(point, 0)
            elif new_x == -1:
                outer_board = self.get_board(self.level - 1)
                count += outer_board.board.get((1, 2), 0)
            elif new_y == -1:
                outer_board = self.get_board(self.level - 1)
                count += outer_board.board.get((2, 1), 0)
            elif new_x == 5:
                outer_board = self.get_board(self.level - 1)
                count += outer_board.board.get((3, 2), 0)
            elif new_y == 5:
                outer_board = self.get_board(self.level - 1)
                count += outer_board.board.get((2, 3), 0)
            else:
                count += self.board.get((new_x, new_y), 0)

        return count

    def print(self):
        for y in range(0, 5):
            print("".join(str(self.board.get((x, y), 0)) for x in range(5)))
        print()


def new_boards(boards):
    min_level = min(boards.keys()) - 1
    max_level = max(boards.keys()) + 1

    new_boards = {}
    for level in range(min_level, max_level + 1):
        new_board = Board(new_boards, level)
        new_boards[level] = new_board

        if level not in boards:
            boards[level] = Board(boards, level)
        board = boards[level]
        for x in range(5):
            for y in range(5):
                if x == y == 2:
                    continue
                num_adjacent = board.num_adjacent([x, y])
                v = board.board.get((x, y), 0)
                old_v = v
                if v:
                    v = num_adjacent == 1
                else:
                    v = num_adjacent in (1, 2)
                new_board.board[x, y] = int(v)

    return new_boards


def counts(boards):
    counts = [sum(board.board.values()) for board in boards.values()]
    return sum(counts)


def main():
    boards = {}
    board = Board.from_string(boards, read_input("day24.txt"))

    for x in range(200):
        boards = new_boards(boards)

    return counts(boards)


if __name__ == "__main__":
    count = main()
    print(count)
