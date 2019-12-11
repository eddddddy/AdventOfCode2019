from solution09 import Program, get_opcode_and_modes, get_value, get_address

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

BLACK = 0
WHITE = 1


def execute_program_blocking(program, inputs, pc=0, relative_base=0):
    def _get_value(parameter_mode, immediate_value, _program):
        return get_value(parameter_mode, immediate_value, _program, relative_base)

    def _get_address(parameter_mode, immediate_value):
        return get_address(parameter_mode, immediate_value, relative_base)

    outputs = []
    while program[pc] != 99:
        opcode, modes = get_opcode_and_modes(program[pc])
        if opcode == 1:
            program[_get_address(modes[2], program[pc + 3])] = _get_value(modes[0], program[pc + 1], program) + \
                                                               _get_value(modes[1], program[pc + 2], program)
            pc += 4
        elif opcode == 2:
            program[_get_address(modes[2], program[pc + 3])] = _get_value(modes[0], program[pc + 1], program) * \
                                                               _get_value(modes[1], program[pc + 2], program)
            pc += 4
        elif opcode == 3:
            if inputs:
                program[_get_address(modes[0], program[pc + 1])] = inputs[0]
                inputs = inputs[1:]
                pc += 2
            else:
                return program, pc, relative_base, outputs, False
        elif opcode == 4:
            outputs.append(_get_value(modes[0], program[pc + 1], program))
            pc += 2
        elif opcode == 5:
            if _get_value(modes[0], program[pc + 1], program):
                pc = _get_value(modes[1], program[pc + 2], program)
            else:
                pc += 3
        elif opcode == 6:
            if not _get_value(modes[0], program[pc + 1], program):
                pc = _get_value(modes[1], program[pc + 2], program)
            else:
                pc += 3
        elif opcode == 7:
            if _get_value(modes[0], program[pc + 1], program) < _get_value(modes[1], program[pc + 2], program):
                program[_get_address(modes[2], program[pc + 3])] = 1
            else:
                program[_get_address(modes[2], program[pc + 3])] = 0
            pc += 4
        elif opcode == 8:
            if _get_value(modes[0], program[pc + 1], program) == _get_value(modes[1], program[pc + 2], program):
                program[_get_address(modes[2], program[pc + 3])] = 1
            else:
                program[_get_address(modes[2], program[pc + 3])] = 0
            pc += 4
        elif opcode == 9:
            relative_base += _get_value(modes[0], program[pc + 1], program)
            pc += 2
        else:
            raise ValueError('Illegal state')
    return program, pc, relative_base, outputs, True


def paint_panel(program, panel):
    current_position = (0, 0)
    current_direction = UP

    pc = 0
    relative_base = 0
    halted = False
    while not halted:
        if current_position in panel:
            current_color = panel[current_position]
        else:
            current_color = BLACK

        program, pc, relative_base, outputs, halted = execute_program_blocking(program, [current_color], pc, relative_base)
        panel[current_position] = outputs[0]
        current_direction = (current_direction + 2 * outputs[1] + 3) % 4

        current_position = (current_position[0] + {UP: 0, RIGHT: 1, LEFT: -1, DOWN: 0}[current_direction],
                            current_position[1] + {UP: -1, RIGHT: 0, LEFT: 0, DOWN: 1}[current_direction])

    return panel


def prettify(panel):
    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    for position in panel:
        xmin = position[0] if position[0] < xmin else xmin
        xmax = position[0] if position[0] > xmax else xmax
        ymin = position[1] if position[1] < ymin else ymin
        ymax = position[1] if position[1] > ymax else ymax

    prettified = ""
    for y in range(ymin, ymax + 1):
        row = ""
        for x in range(xmin, xmax + 1):
            if (x, y) in panel:
                row += '.' if panel[(x, y)] == BLACK else '#'
            else:
                row += '.'
        prettified += f'{row}\n'

    return prettified


def main():
    with open('input11.txt') as f:
        program = [int(num) for num in f.readline().strip().split(',')]

    # Part 1
    print(len(paint_panel(Program(program[:]), {})))

    # Part 2
    print(prettify(paint_panel(Program(program[:]), {(0, 0): WHITE})))


if __name__ == '__main__':
    main()
