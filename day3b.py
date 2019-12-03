def read_input():
    with open("day3.txt") as f:
        l1 = f.readline().strip().split(",")
        l2 = f.readline().strip().split(",")
        return l1, l2


def generate_points(instructions):
    points = {}
    counter = 0
    current_point = (0, 0)

    for instruction in instructions:
        direction = instruction[0]
        number = int(instruction[1:])
        move = moves[direction]
        for x in range(number):
            counter += 1
            current_point = move(current_point)
            points.setdefault(current_point, counter)

    return points


def up(point):
    return (point[0], point[1] + 1)


def down(point):
    return (point[0], point[1] - 1)


def left(point):
    return (point[0] - 1, point[1])


def right(point):
    return (point[0] + 1, point[1])


moves = {"U": up, "D": down, "L": left, "R": right}


def main():
    l1, l2 = read_input()

    points1 = generate_points(l1)
    points2 = generate_points(l2)
    crossings = points1.keys() & points2.keys()
    minimum_distance = min(points1[x] + points2[x] for x in crossings)
    print(minimum_distance)


if __name__ == "__main__":
    main()
