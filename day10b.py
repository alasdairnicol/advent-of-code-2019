#!/usr/bin/env python
import itertools
import math
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


def get_site(asteroids):
    max_seen = 0
    max_site = None
    max_vectors = None

    for site in asteroids:
        vectors = get_vectors_for_site(asteroids, site)
        if len(vectors) > max_seen:
            max_seen = len(vectors)
            max_site = site
            max_vectors = vectors

    sort_lists(max_site, max_vectors)

    return max_site, max_vectors


def main():
    asteroids = get_asteroids(read_input("day10.txt"))
    site, vectors = get_site(asteroids)

    count = 0

    keys = sorted(vectors.keys(), key=lambda x: vector_to_rad(*x))

    for key in itertools.cycle(keys):
        if vectors[key]:
            asteroid = vectors[key].pop(0)
            count += 1
            if count == 200:
                break

    return asteroid


def sort_lists(site, sites_dict):
    for v in sites_dict.values():
        v.sort(key=lambda x: abs(x[0] - site[0]) + abs(x[1] - site[1]))


def get_vectors_for_site(asteroids, site):
    angles = defaultdict(list)
    for asteroid in asteroids:
        if asteroid == site:
            continue

        distance = (asteroid[0] - site[0], asteroid[1] - site[1])

        divisor = abs(gcd(*distance))
        angle = (distance[0] // divisor, distance[1] // divisor)
        angles[angle].append(asteroid)
    return angles


def vector_to_rad(x, y):
    if y == 0 and x < 0:
        rad = 3 * math.pi / 2
    elif y == 0 and x > 0:
        rad = math.pi / 2
    elif y < 0:
        rad = math.atan(-x / y)
        if x < 0:
            rad += 2 * math.pi
    elif y > 0:
        rad = math.pi - math.atan(x / y)
    return rad


if __name__ == "__main__":
    asteroid = main()
    print(asteroid[0] * 100 + asteroid[1])
