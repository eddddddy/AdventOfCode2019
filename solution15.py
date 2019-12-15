from enum import Enum

from solution09 import Program
from solution11 import execute_program_blocking


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def opposite(self):
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST
        }[self]


class Position:

    def __init__(self, x, y):
        self.position = (x, y)

    def __repr__(self):
        return f'({self.position[0]}, {self.position[1]})'

    def __hash__(self):
        return hash(self.position)

    def __eq__(self, other):
        return self.position == other.position

    def step(self, direction):
        return {
            Direction.NORTH: Position(self.position[0], self.position[1] - 1),
            Direction.SOUTH: Position(self.position[0], self.position[1] + 1),
            Direction.WEST: Position(self.position[0] - 1, self.position[1]),
            Direction.EAST: Position(self.position[0] + 1, self.position[1])
        }[direction]


NORTH = Direction.NORTH
SOUTH = Direction.SOUTH
WEST = Direction.WEST
EAST = Direction.EAST

WALL = 0
EMPTY = 1
OS = 2


def get_last_matching_index(l1, l2):
    last_index = -1
    while True:
        try:
            if l1[last_index + 1] == l2[last_index + 1]:
                last_index += 1
            else:
                break
        except IndexError:
            break
    return last_index if last_index >= 0 else None


def map_and_find_oxygen_system(program):
    area = {Position(0, 0): EMPTY}
    directions_from_start = {Position(0, 0): []}
    to_explore = []
    position_to_check = Position(0, 0)
    steps_from_start = []

    os_location = None

    pc = 0
    relative_base = 0

    while True:
        directions_to_check = [NORTH, SOUTH, WEST, EAST]
        for direction in directions_to_check:
            if position_to_check.step(direction) in area:
                continue

            program, pc, relative_base, outputs, _ = \
                execute_program_blocking(program, [direction.value], pc, relative_base)
            if WALL in outputs:
                area[position_to_check.step(direction)] = WALL
            elif EMPTY in outputs:
                to_explore.append(position_to_check.step(direction))
                area[position_to_check.step(direction)] = EMPTY
                directions_from_start[position_to_check.step(direction)] = steps_from_start[:] + [direction]
                program, pc, relative_base, outputs, _ = \
                    execute_program_blocking(program, [direction.opposite().value], pc, relative_base)
            else:
                to_explore.append(position_to_check.step(direction))
                area[position_to_check.step(direction)] = OS
                directions_from_start[position_to_check.step(direction)] = steps_from_start[:] + [direction]
                os_location = position_to_check.step(direction)
                program, pc, relative_base, outputs, _ = \
                    execute_program_blocking(program, [direction.opposite().value], pc, relative_base)

        if not to_explore:
            return area, directions_from_start, os_location

        position_to_check = to_explore[0]
        to_explore = to_explore[1:]

        last_index = get_last_matching_index(steps_from_start, directions_from_start[position_to_check])

        if last_index is not None:
            for direction in steps_from_start[:last_index:-1]:
                program, pc, relative_base, _, _ = \
                    execute_program_blocking(program, [direction.opposite().value], pc, relative_base)

            steps_from_start = directions_from_start[position_to_check]
            for direction in steps_from_start[last_index + 1:]:
                program, pc, relative_base, _, _ = execute_program_blocking(program, [direction.value], pc,
                                                                            relative_base)
            continue

        for direction in steps_from_start[::-1]:
            program, pc, relative_base, _, _ = \
                execute_program_blocking(program, [direction.opposite().value], pc, relative_base)

        steps_from_start = directions_from_start[position_to_check]
        for direction in steps_from_start:
            program, pc, relative_base, _, _ = execute_program_blocking(program, [direction.value], pc, relative_base)


def get_time_to_fill(area, os_position):
    time = 0
    oxygen_positions = {os_position}

    while oxygen_positions:
        directions = [NORTH, SOUTH, EAST, WEST]
        new_oxygen_positions = set()

        for oxygen_position in oxygen_positions:
            for direction in directions:
                if area[oxygen_position.step(direction)] == EMPTY:
                    area[oxygen_position.step(direction)] = OS
                    new_oxygen_positions.add(oxygen_position.step(direction))

        oxygen_positions = new_oxygen_positions
        time += 1

    return time - 1


def main():
    with open('input15.txt') as f:
        program = [int(num) for num in f.readline().split(',')]

    area, directions, os_position = map_and_find_oxygen_system(Program(program[:]))

    # Part 1
    print(len(directions[os_position]))

    # Part 2
    print(get_time_to_fill(area, os_position))


if __name__ == '__main__':
    main()
