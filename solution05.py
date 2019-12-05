def get_opcode_and_modes(instruction):
    opcode = instruction % 100
    num_parameters = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3}[opcode]

    if len(str(instruction)) < 2:
        return opcode, [0] * num_parameters

    parameter_modes = list(map(int, str(instruction)[:-2][::-1]))

    if num_parameters > len(parameter_modes):
        parameter_modes.extend([0] * (num_parameters - len(parameter_modes)))

    return opcode, parameter_modes


def get_value(parameter_mode, immediate_value, program):
    return program[immediate_value] if parameter_mode == 0 else immediate_value


def execute_program(program, inputs):
    pc = 0
    outputs = []
    while program[pc] != 99:
        opcode, modes = get_opcode_and_modes(program[pc])
        if opcode == 1:
            program[program[pc + 3]] = get_value(modes[0], program[pc + 1], program) + \
                                       get_value(modes[1], program[pc + 2], program)
            pc += 4
        elif opcode == 2:
            program[program[pc + 3]] = get_value(modes[0], program[pc + 1], program) * \
                                       get_value(modes[1], program[pc + 2], program)
            pc += 4
        elif opcode == 3:
            program[program[pc + 1]] = inputs[0]
            inputs = inputs[1:]
            pc += 2
        elif opcode == 4:
            outputs.append(get_value(modes[0], program[pc + 1], program))
            pc += 2
        elif opcode == 5:
            if get_value(modes[0], program[pc + 1], program):
                pc = get_value(modes[1], program[pc + 2], program)
            else:
                pc += 3
        elif opcode == 6:
            if not get_value(modes[0], program[pc + 1], program):
                pc = get_value(modes[1], program[pc + 2], program)
            else:
                pc += 3
        elif opcode == 7:
            if get_value(modes[0], program[pc + 1], program) < get_value(modes[1], program[pc + 2], program):
                program[program[pc + 3]] = 1
            else:
                program[program[pc + 3]] = 0
            pc += 4
        elif opcode == 8:
            if get_value(modes[0], program[pc + 1], program) == get_value(modes[1], program[pc + 2], program):
                program[program[pc + 3]] = 1
            else:
                program[program[pc + 3]] = 0
            pc += 4
        else:
            raise ValueError('Illegal state')
    return program, outputs


def get_last_output(program, inputs):
    result, outputs = execute_program(program, inputs)
    return outputs[-1]


def main():
    with open('input05.txt') as f:
        program = [int(num) for num in f.readline().split(',')]

    # Part 1
    print(get_last_output(program[:], [1]))

    # Part 2
    print(get_last_output(program[:], [5]))


if __name__ == '__main__':
    main()
