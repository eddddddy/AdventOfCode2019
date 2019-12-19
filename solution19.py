from solution09 import Program, execute_program

WINDOW_SIZE = 50
SANTA_SHIP_SIZE = 100
AFFECTED = '#'
NOT_AFFECTED = '.'


def find_tractor_beam_boundaries_by_row(program_instructions, limit):
    boundaries = {0: (0, 0), 5: (6, 6)}
    previous_first_affected_point = 6
    previous_last_affected_point = 6
    for y in range(6, limit):
        first, last = None, None
        for offset in range(1, 3):
            _, outputs = execute_program(Program(program_instructions[:]),
                                         [previous_first_affected_point + offset, y])
            if 1 in outputs:
                first = previous_first_affected_point + offset
                break
        for offset in range(2, 0, -1):
            _, outputs = execute_program(Program(program_instructions[:]),
                                         [previous_last_affected_point + offset, y])
            if 1 in outputs:
                last = previous_last_affected_point + offset
                break

        previous_first_affected_point = first
        previous_last_affected_point = last
        boundaries[y] = (first, last)
    return boundaries


def get_num_affected_points_in_window(program_instructions, window_size):
    boundaries = find_tractor_beam_boundaries_by_row(program_instructions, window_size)
    count = 0
    for y in range(window_size):
        if y not in boundaries:
            continue
        count += min(window_size - 1, boundaries[y][1]) - min(boundaries[y][0], window_size) + 1
    return count


def get_closest_embedded_square_coordinates(program_instructions, square_size):
    limit = square_size * 15
    boundaries = find_tractor_beam_boundaries_by_row(program_instructions, limit)
    for y in range(limit):
        if y not in boundaries or y + square_size - 1 not in boundaries:
            continue
        first, last = boundaries[y]
        first_down, last_down = boundaries[y + square_size - 1]
        for x in range(first, last - square_size + 2):
            if x >= first_down and x + square_size - 1 <= last_down:
                return x, y


def main():
    with open('input19.txt') as f:
        program = [int(num) for num in f.readline().split(',')]

    # Part 1
    print(get_num_affected_points_in_window(program, WINDOW_SIZE))

    # Part 2
    x, y = get_closest_embedded_square_coordinates(program, SANTA_SHIP_SIZE)
    print(10000 * x + y)


if __name__ == '__main__':
    main()
