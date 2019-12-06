def get_orbits():
    """
    Return a map where the values are the objects orbited
    """
    orbits = {}
    with open("day6.txt") as f:
        for line in f.readlines():
            a, b = line.strip().split(")")
            orbits[b] = a
    return orbits


def get_num_orbits(obj, orbits, num_orbits):
    if obj == "COM":
        return 0
    if obj not in num_orbits:
        if obj == "COM":
            num_orbits[obj] = 0
        else:
            num_orbits[obj] = get_num_orbits(orbits[obj], orbits, num_orbits) + 1
    return num_orbits[obj]


def main():
    orbits = get_orbits()
    num_orbits = {}

    for obj in orbits:
        get_num_orbits(obj, orbits, num_orbits)

    print(sum(num_orbits.values()))


if __name__ == "__main__":
    main()
