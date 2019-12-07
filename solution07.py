from itertools import permutations

from solution05 import get_opcode_and_modes, get_value


def execute_program_blocking(program, inputs, pc=0):
    """
    :return: program, pc, outputs, halted
    """
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
            if inputs:
                program[program[pc + 1]] = inputs[0]
                inputs = inputs[1:]
                pc += 2
            else:
                return program, pc, outputs, False
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
    return program, pc, outputs, True


def run_amplifiers(perm, program):
    programs = [program[:], program[:], program[:], program[:], program[:]]
    pcs = [0, 0, 0, 0, 0]
    outputs = [[], [], [], [], []]
    halts = [False, False, False, False, False]

    for amp in range(5):
        program, pc, output, halted = execute_program_blocking(programs[amp], [perm[amp]], 0)
        programs[amp] = program
        pcs[amp] = pc

    outputs[4] = [0]
    current_amp = 0
    while not halts[current_amp]:
        program, pc, output, halted = execute_program_blocking(programs[current_amp],
                                                               outputs[current_amp - 1],
                                                               pcs[current_amp])
        programs[current_amp] = program
        pcs[current_amp] = pc
        outputs[current_amp] = output
        halts[current_amp] = halted
        current_amp = (current_amp + 1) % 5

    return outputs[4][0]


def find_largest_signal(program, phase_settings):
    phase_settings = permutations(phase_settings)
    best = -1
    for setting in phase_settings:
        signal = run_amplifiers(setting, program)
        if signal > best:
            best = signal
    return best


def main():
    with open('input07.txt') as f:
        program = [int(num) for num in f.readline().split(',')]

    # Part 1
    print(find_largest_signal(program, [0, 1, 2, 3, 4]))

    # Part 2
    print(find_largest_signal(program, [5, 6, 7, 8, 9]))


if __name__ == '__main__':
    main()
