initial_noun = 12
initial_verb = 2

target_output = 19690720


def execute_program(program):
    pc = 0
    while program[pc] != 99:
        if program[pc] == 1:
            program[program[pc + 3]] = program[program[pc + 1]] + program[program[pc + 2]]
        elif program[pc] == 2:
            program[program[pc + 3]] = program[program[pc + 1]] * program[program[pc + 2]]
        else:
            raise ValueError('Illegal state')
        pc += 4
    return program[0]


def main_part1():
    with open('input02.txt') as f:
        program = [int(num) for num in f.readline().split(',')]

        program[1] = initial_noun
        program[2] = initial_verb

        return execute_program(program)


def main_part2():
    with open('input02.txt') as f:
        program = [int(num) for num in f.readline().split(',')]

        for noun in range(100):
            for verb in range(100):
                program_copy = program[:]
                program_copy[1] = noun
                program_copy[2] = verb

                if execute_program(program_copy) == target_output:
                    return 100 * noun + verb


def main():
    # Part 1
    print(main_part1())

    # Part 2
    print(main_part2())


if __name__ == '__main__':
    main()
