from solution09 import Program, execute_program

SCAFFOLD = '#'


def get_exterior_grid(output):
    grid = []
    curr_row = []
    for ascii_code in output:
        if ascii_code == ord('\n'):
            if curr_row:
                grid.append(curr_row)
                curr_row = []
        else:
            curr_row.append(ascii_code)
    return grid


def get_intersections(grid):
    height = len(grid)
    width = len(grid[0])
    intersections = []

    for i in range(height):
        for j in range(width):
            if grid[i][j] != ord(SCAFFOLD):
                continue
            neighbour_scaffolds = 0
            for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                try:
                    if grid[i + di][j + dj] == ord(SCAFFOLD):
                        neighbour_scaffolds += 1
                except IndexError:
                    continue
            if neighbour_scaffolds > 2:
                intersections.append((j, i))

    return intersections


def sum_alignment_parameters(intersections):
    total = 0
    for intersection in intersections:
        total += intersection[0] * intersection[1]
    return total

    
def to_ascii(s):
    return [ord(char) for char in s + '\n']


def collect_dust(program):
    A = to_ascii('R,8,L,10,R,8')
    B = to_ascii('R,12,R,8,L,8,L,12')
    C = to_ascii('L,12,L,10,L,8')
    routine = to_ascii('A,B,A,C,A,B,C,C,A,B')
    video = to_ascii('n')

    _, output = execute_program(program, routine + A + B + C + video)
    return output[-1]


def main():
    with open('input17.txt') as f:
        program = [int(num) for num in f.readline().split(',')]

    # Part 1
    _, output = execute_program(Program(program[:]), [])
    print(sum_alignment_parameters(get_intersections(get_exterior_grid(output))))

    # Part 2
    print(collect_dust(Program([2] + program[1:])))


if __name__ == '__main__':
    main()
