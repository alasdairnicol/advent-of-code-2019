DIMENSIONS = (25, 6)


def count_digits(l, digit):
    return sum([len([y for y in x if y == digit]) for x in l])


def count_zeroes(l):
    return count_digits(l, 0)


def get_pixel(layers, x, y):
    for layer in layers:
        pixel = layer[y][x]
        if pixel in (0, 1):
            return pixel


def main():
    # get layers
    values = iter(read_input())
    x, y = DIMENSIONS

    layers = []

    while True:
        try:
            layer = [[next(values) for _ in range(x)] for _ in range(y)]
            layers.append(layer)
        except StopIteration:
            break

    combined = [[2] * x for j in range(y)]

    for j in range(y):
        for i in range(x):
            combined[j][i] = get_pixel(layers, i, j)

    return combined


def read_input():
    with open("day8.txt") as f:
        return [int(x) for x in f.read().rstrip()]


if __name__ == "__main__":
    combined = main()
    for row in combined:
        print("".join("x" if x else " " for x in row))
