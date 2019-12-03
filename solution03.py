from typing import List, Dict, Tuple
from functools import reduce


def get_wire_points(path: List[str]) -> Dict[Tuple[int, int], int]:
    curr_point = [0, 0]
    curr_length = 0
    points: Dict[Tuple[int, int], int] = {}
    for line in path:
        direction, distance = line[0], int(line[1:])
        if direction == 'R':
            new_points = {p: curr_length + p[0] - curr_point[0]
                          for p in map(tuple, zip(range(curr_point[0], curr_point[0] + distance),
                                                  [curr_point[1]] * distance))}
            new_points = {p: d for p, d in new_points.items() if p not in points}
            points = {**points, **new_points}
            curr_point[0] += distance
            curr_length += distance
        elif direction == 'U':
            new_points = {p: curr_length + p[1] - curr_point[1]
                          for p in map(tuple, zip([curr_point[0]] * distance,
                                                  range(curr_point[1], curr_point[1] + distance)))}
            new_points = {p: d for p, d in new_points.items() if p not in points}
            points = {**points, **new_points}
            curr_point[1] += distance
            curr_length += distance
        elif direction == 'L':
            new_points = {p: curr_length + curr_point[0] - p[0]
                          for p in map(tuple, zip(range(curr_point[0], curr_point[0] - distance, -1),
                                                  [curr_point[1]] * distance))}
            new_points = {p: d for p, d in new_points.items() if p not in points}
            points = {**points, **new_points}
            curr_point[0] -= distance
            curr_length += distance
        elif direction == 'D':
            new_points = {p: curr_length + curr_point[1] - p[1]
                          for p in map(tuple, zip([curr_point[0]] * distance,
                                                  range(curr_point[1], curr_point[1] - distance, -1)))}
            new_points = {p: d for p, d in new_points.items() if p not in points}
            points = {**points, **new_points}
            curr_point[1] -= distance
            curr_length += distance
    return points


def intersection_points(points1: Dict[Tuple[int, int], int],
                        points2: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], int]:
    points = {}
    for point in points1.keys():
        if point != (0, 0) and point in points2:
            points[point] = points1[point] + points2[point]
    return points


def min_distance_point(points: Dict[Tuple[int, int], int]) -> Tuple[int, int]:
    return reduce(lambda p1, p2: p1 if abs(p1[0]) + abs(p1[1]) < abs(p2[0]) + abs(p2[1]) else p2, points.keys())


def min_path_length(points: Dict[Tuple[int, int], int]) -> int:
    return min(points.values())


def main():
    with open('input03.txt') as f:
        wire1 = f.readline().split(',')
        wire2 = f.readline().split(',')
        points1 = get_wire_points(wire1)
        points2 = get_wire_points(wire2)
        int_points = intersection_points(points1, points2)

    # Part 1
    min_point = min_distance_point(int_points)
    print(abs(min_point[0]) + abs(min_point[1]))

    # Part 2
    print(min_path_length(int_points))


if __name__ == '__main__':
    main()
