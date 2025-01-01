#!/usr/bin/env python
import functools
import copy


def calc_energy(positions, velocities):
    return sum(
        sum(abs(x) for x in position) * sum(abs(y) for y in velocity)
        for position, velocity in zip(positions, velocities)
    )


def do_step(positions, velocities, axis):
    # Do gravity
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            if positions[i][axis] > positions[j][axis]:
                velocities[i][axis] -= 1
                velocities[j][axis] += 1
            elif positions[i][axis] < positions[j][axis]:
                velocities[i][axis] += 1
                velocities[j][axis] -= 1

    # Add velocities
    for i in range(len(positions)):
        positions[i][axis] += velocities[i][axis]


def get_axis_state(positions, velocities, axis):
    return [p[axis] for p in positions] + [v[axis] for v in velocities]


def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x


def lcm(x, y):
    return x * y // gcd(x, y)


def main():
    positions = [
        [-3, 10, -1],
        [-12, -10, -5],
        [-9, 0, 10],
        [7, -5, -3],
    ]

    velocities = [[0, 0, 0] for _ in positions]
    initial_state = [get_axis_state(positions, velocities, x) for x in range(3)]

    periods = [None, None, None]

    num_steps = 0

    # Calculate the period for each axis
    for axis in [0, 1, 2]:
        num_steps = 0
        initial_state = get_axis_state(positions, velocities, axis)

        while True:
            do_step(positions, velocities, axis)
            num_steps += 1
            if get_axis_state(positions, velocities, axis) == initial_state:
                periods[axis] = num_steps
                break

    # The period for the entire system is the lcm of the periods of the axes
    period = functools.reduce(lcm, periods)
    return period


if __name__ == "__main__":
    period = main()
    print(period)
