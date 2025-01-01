#!/usr/bin/env python
from collections import defaultdict


def get_asteroids(lines):
    asteroids = []
    for j, line in enumerate(lines):
        for i, value in enumerate(line):
            if value == "#":
                asteroids.append((i, j))
            elif value != ".":
                raise ValueError("Unexpected value %s" % value)
    return asteroids


def read_input(filename):
    with open(filename) as f:
        return f.read().split()


def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x


def main():
    asteroids = get_asteroids(read_input("day10.txt"))
    return max(len(get_vectors_for_site(asteroids, site)) for site in asteroids)


def get_vectors_for_site(asteroids, site):
    vectors = defaultdict(list)
    for asteroid in asteroids:
        if asteroid == site:
            continue

        distance = (asteroid[0] - site[0], asteroid[1] - site[1])

        divisor = abs(gcd(*distance))
        vector = (distance[0] // divisor, distance[1] // divisor)
        vectors[vector].append(asteroid)
    return vectors


if __name__ == "__main__":
    count = main()
    print(count)
