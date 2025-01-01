def calc_energy(positions, velocities):
    return sum(
        sum(abs(x) for x in position) * sum(abs(y) for y in velocity)
        for position, velocity in zip(positions, velocities)
    )


def do_step(positions, velocities):
    # Do gravity
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            for x in range(3):
                if positions[i][x] > positions[j][x]:
                    velocities[i][x] -= 1
                    velocities[j][x] += 1
                elif positions[i][x] < positions[j][x]:
                    velocities[i][x] += 1
                    velocities[j][x] -= 1

    # Add velocities
    for i in range(len(positions)):
        positions[i] = [(x + y) for x, y in zip(positions[i], velocities[i])]


def main():
    positions = [
        [-3, 10, -1],
        [-12, -10, -5],
        [-9, 0, 10],
        [7, -5, -3],
    ]

    velocities = [[0, 0, 0] for _ in positions]

    num_steps = 1000

    for step in range(1, num_steps + 1):
        do_step(positions, velocities)

    energy = calc_energy(positions, velocities)
    return energy


if __name__ == "__main__":
    energy = main()
    print(energy)
