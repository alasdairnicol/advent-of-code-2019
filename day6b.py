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


def get_orbit_list(obj, orbits):
    if obj == "COM":
        return []
    else:
        return [orbits[obj]] + get_orbit_list(orbits[obj], orbits)


def main():
    orbits = get_orbits()
    num_orbits = {}

    you = get_orbit_list("YOU", orbits)
    santa = get_orbit_list("SAN", orbits)

    while you[-1] == santa[-1]:
        you.pop()
        santa.pop()

    # Moving you len(you) steps gets you to parent node,
    # then moving len(santa) steps get you to same obj as Santa
    num_hops = len(you) + len(santa)

    print(num_hops)


if __name__ == "__main__":
    main()
