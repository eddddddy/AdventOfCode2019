from solution09 import Program
from solution11 import execute_program_blocking

BLOCK_TILE = 2
PADDLE = 3
BALL = 4


def get_grid(program):
    grid = {}
    _, _, _, outputs, _ = execute_program_blocking(program, [])
    while outputs:
        grid[(outputs[0], outputs[1])] = outputs[2]
        outputs = outputs[3:]

    return grid


def determine_input(ball_position, paddle_position):
    if ball_position[0] < paddle_position[0]:
        return -1
    elif ball_position[0] == paddle_position[0]:
        return 0
    else:
        return 1


def simulate(program):
    def _update_state():
        nonlocal score, ball_position, paddle_position, outputs
        while outputs:
            if outputs[0] == -1 and outputs[1] == 0:
                score = outputs[2]
            else:
                grid[(outputs[0], outputs[1])] = outputs[2]
                if outputs[2] == BALL:
                    ball_position = (outputs[0], outputs[1])
                elif outputs[2] == PADDLE:
                    paddle_position = (outputs[0], outputs[1])
            outputs = outputs[3:]

    grid = {}
    score = 0
    ball_position = (0, 0)
    paddle_position = (0, 0)

    program, pc, relative_base, outputs, halted = execute_program_blocking(program, [])
    _update_state()

    while not halted:
        program, pc, relative_base, outputs, halted = execute_program_blocking(
            program, [determine_input(ball_position, paddle_position)], pc, relative_base
        )
        _update_state()

    return score


def main():
    with open('input13.txt') as f:
        program = [int(num) for num in f.readline().split(',')]

    # Part 1
    print(list(get_grid(Program(program[:])).values()).count(BLOCK_TILE))

    # Part 2
    print(simulate(Program([2] + program[1:])))


if __name__ == '__main__':
    main()
