from itertools import groupby

import numpy as np

n = 200


def polarize(point1, point2):
    x = point2[0] - point1[0]
    y = point1[1] - point2[1]
    return np.sqrt(x ** 2 + y ** 2), (5 * np.pi / 2 - np.arctan2(y, x)) % (2 * np.pi)


def unpolarize(r, theta):
    theta = np.pi / 2 - theta
    return int(np.floor(r * np.cos(theta) + 0.5)), int(np.floor(r * np.sin(theta) + 0.5))


def get_num_visible_asteroids(location, other_locations):
    return len(set(map(lambda other: polarize(location, other)[1], other_locations)))


def get_max_num_visible_asteroids(locations):
    max_visible = 0
    max_location = None
    for _ in range(len(locations)):
        num_visible = get_num_visible_asteroids(locations[0], locations[1:])
        max_visible, max_location = (num_visible, locations[0]) \
            if num_visible > max_visible else (max_visible, max_location)
        locations = [locations[-1]] + locations[:-1]
    return max_visible, max_location


def get_nth_vaporization_location(laser_location, other_locations):
    other_locations = list(map(lambda other: polarize(laser_location, other), other_locations))
    other_locations = sorted(other_locations, key=lambda other: other[0])
    other_locations = sorted(other_locations, key=lambda other: other[1])

    vaporization_order = []
    groups = [list(group) for key, group in groupby(other_locations, lambda other: other[1])]

    while groups:
        vaporization_order.extend([group[0] for group in groups])

        if len(vaporization_order) >= n:
            break

        groups = [group[1:] for group in groups]
        groups = [group for group in groups if group]

    nth_location = unpolarize(*vaporization_order[n - 1])
    return nth_location[0] + laser_location[0], laser_location[1] - nth_location[1]


def get_asteroid_locations(map_data):
    height = len(map_data)
    width = len(map_data[0])
    locations = []
    for i in range(height):
        for j in range(width):
            if map_data[i][j] == '#':
                locations.append((j, i))
    return locations


def main():
    with open('input10.txt') as f:
        map_data = [list(line) for line in f.readlines()]
        locations = get_asteroid_locations(map_data)

    # Part 1
    max_visible, max_location = get_max_num_visible_asteroids(locations)
    print(max_visible)

    # Part 2
    other_locations = [location for location in locations if location != max_location]
    nth_location = get_nth_vaporization_location(max_location, other_locations)
    print(nth_location[0] * 100 + nth_location[1])


if __name__ == '__main__':
    main()
