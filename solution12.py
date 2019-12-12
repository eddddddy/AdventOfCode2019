import math

import numpy as np

NUM_STEPS = 1000


def lcm(*args):
    k = args[0]
    args = args[1:]
    while args:
        k = k * args[0] // math.gcd(k, args[0])
        args = args[1:]
    return k


def increment(positions, velocities):
    for i in range(4):
        velocity_offset = np.array([0, 0, 0])
        position = positions[i]
        for j in range(4):
            if i != j:
                other_position = positions[j]
                velocity_offset += ((other_position > position).astype(int) -
                                    (position > other_position).astype(int))
        velocities[i] = velocities[i] + velocity_offset

    for i in range(4):
        positions[i] += velocities[i]

    return positions, velocities


def total_energy(positions, velocities):
    total = 0
    for i in range(4):
        total += np.sum(np.abs(positions[i])) * np.sum(np.abs(velocities[i]))
    return total


def get_energy_at_step(positions, velocities, step):
    positions = [np.copy(position) for position in positions]
    velocities = [np.copy(velocity) for velocity in velocities]

    for i in range(step):
        positions, velocities = increment(positions, velocities)

    return total_energy(positions, velocities)


def get_period(positions, velocities, dimension):
    positions = [np.copy(position) for position in positions]
    velocities = [np.copy(velocity) for velocity in velocities]

    seen = {tuple([position[dimension] for position in positions] +
                  [velocity[dimension] for velocity in velocities]): 0}
    step = 0
    while True:
        positions, velocities = increment(positions, velocities)
        step += 1
        if tuple([position[dimension] for position in positions] +
                 [velocity[dimension] for velocity in velocities]) in seen:
            return seen[tuple([position[dimension] for position in positions] +
                              [velocity[dimension] for velocity in velocities])], step

        seen[tuple([position[dimension] for position in positions] +
                   [velocity[dimension] for velocity in velocities])] = step


def main():
    with open('input12.txt') as f:
        positions = []
        for _ in range(4):
            line = f.readline().strip().lstrip('<').rstrip('>')
            components = [component.strip() for component in line.split(',')]
            positions.append(np.array([int(component[2:]) for component in components]))

    # Part 1
    print(get_energy_at_step(positions[:], [np.array([0, 0, 0])] * 4, NUM_STEPS))

    # Part 2
    print(lcm(
        get_period(positions[:], [np.array([0, 0, 0])] * 4, 0)[1],
        get_period(positions[:], [np.array([0, 0, 0])] * 4, 1)[1],
        get_period(positions[:], [np.array([0, 0, 0])] * 4, 2)[1]
    ))


if __name__ == '__main__':
    main()
