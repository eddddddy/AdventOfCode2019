from solution09 import Program, execute_program
from solution17 import to_ascii

    
def run_springdroid(program, spring_script):
    return execute_program(program, spring_script)[1][-1]
    
    
def main_part1(program):
    return run_springdroid(program, to_ascii('\n'.join([
        'NOT J T', 
        'AND A T', 
        'AND B T', 
        'AND C T', 
        'NOT T J', 
        'AND D J', 
        'WALK'])))
        
        
def main_part2(program):
    return run_springdroid(program, to_ascii('\n'.join([
        'NOT J T',
        'OR T J',
        'AND A T',
        'AND B T',
        'AND C T',
        'NOT T T',
        'AND E J',
        'OR H J',
        'AND T J',
        'AND D J',
        'RUN'])))


def main():
    with open('input21.txt') as f:
        program = [int(num) for num in f.readline().split(',')]
        
    # Part 1
    print(main_part1(Program(program[:])))
    
    # Part 2
    print(main_part2(Program(program[:])))
    
    
if __name__ == '__main__':
    main()
