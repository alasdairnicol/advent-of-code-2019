DIMENSIONS = (25, 6)


def count_digits(l, digit):
    return sum([len([y for y in x if y == digit]) for x in l])


def count_zeroes(l):
    return count_digits(l, 0)


def main():
    values = iter(read_input())
    x, y = DIMENSIONS

    layers = []

    while True:
        try:
            layer = [[next(values) for _ in range(x)] for _ in range(y)]
            layers.append(layer)
        except StopIteration:
            break

    min_layer = None
    min_zeroes = x * y + 1

    for layer in layers:
        num_zeroes = count_zeroes(layer)
        if num_zeroes < min_zeroes:
            min_layer = layer
            min_zeroes = num_zeroes

    return count_digits(min_layer, 2) * count_digits(min_layer, 1)


def read_input():
    with open("day8.txt") as f:
        return [int(x) for x in f.read().rstrip()]


if __name__ == "__main__":
    count = main()
    print(count)
