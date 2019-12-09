class Program:
    def __init__(self, instruction_mem):
        self.instruction_mem = instruction_mem
        self.extra_mem = {}

    def __len__(self):
        return len(self.instruction_mem)

    def __getitem__(self, item):
        try:
            return self.instruction_mem[item]
        except IndexError:
            if item in self.extra_mem:
                return self.extra_mem[item]
            else:
                self.extra_mem[item] = 0
                return 0

    def __setitem__(self, key, value):
        try:
            self.instruction_mem[key] = value
        except IndexError:
            self.extra_mem[key] = value


def get_opcode_and_modes(instruction):
    opcode = instruction % 100
    num_parameters = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1}[opcode]

    if len(str(instruction)) < 2:
        return opcode, [0] * num_parameters

    parameter_modes = list(map(int, str(instruction)[:-2][::-1]))

    if num_parameters > len(parameter_modes):
        parameter_modes.extend([0] * (num_parameters - len(parameter_modes)))

    return opcode, parameter_modes


def get_value(parameter_mode, immediate_value, program, relative_base):
    if parameter_mode == 0:
        return program[immediate_value]
    elif parameter_mode == 1:
        return immediate_value
    else:
        return program[immediate_value + relative_base]


def get_address(parameter_mode, immediate_value, relative_base):
    if parameter_mode == 0:
        return immediate_value
    else:
        return immediate_value + relative_base


def execute_program(program, inputs):
    pc = 0
    relative_base = 0

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
            program[_get_address(modes[0], program[pc + 1])] = inputs[0]
            inputs = inputs[1:]
            pc += 2
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
    return program, outputs


def get_last_output(program, inputs):
    result, outputs = execute_program(program, inputs)
    return outputs[-1]


def main():
    with open('input09.txt') as f:
        program = [int(num) for num in f.readline().split(',')]

    # Part 1
    print(get_last_output(Program(program[:]), [1]))

    # Part 2
    print(get_last_output(Program(program[:]), [2]))


if __name__ == '__main__':
    main()
