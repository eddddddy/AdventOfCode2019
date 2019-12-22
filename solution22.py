from enum import Enum
from copy import copy

TOTAL_CARDS_PART1 = 10007
TOTAL_CARDS_PART2 = 119315717514047

CARD_OF_INTEREST = 2019
POSITION_OF_INTEREST = 2020
NUM_SHUFFLES = 101741582076661


def extended_gcd(a, b):
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
            
    assert b == 1
    return x0, y0


class TechniqueType(Enum):
    NEW = 1
    CUT = 2
    DEAL = 3
    
    
class Technique:
    def __init__(self, technique_type, N=None):
        self.technique_type = technique_type
        self.N = N
        
        
class LinearFunc:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def compose(self, other):
        self.a = self.a * other.a
        self.b = self.b * other.a + other.b
        
    def reduce(self, n):
        self.a = self.a % n
        self.b = self.b % n
        
    def evaluate(self, arg):
        return self.a * arg + self.b
        
    def evaluate_inverse(self, arg, n):
        return ((arg - self.b + n) * extended_gcd(self.a, n)[0] % n)
        
    def repeat(self, k):
        self.a, self.b = self.a ** k, (self.a ** k - 1) // (self.a - 1) * self.b
        return self
        
    def repeat_and_reduce(self, k, n):
        func = copy(self)
        self.a, self.b = 1, 0

        while k:
            self.compose(copy(func).repeat(k % 10))
            self.reduce(n)
        
            func = copy(func)
            func.repeat(10)
            func.reduce(n)
            
            k = k // 10
        
        
def get_linear_func(shuffle):
    func = LinearFunc(1, 0)
    for technique in shuffle:
        if technique.technique_type == TechniqueType.NEW:
            func.compose(LinearFunc(-1, -1))
        elif technique.technique_type == TechniqueType.CUT:
            func.compose(LinearFunc(1, -1 * technique.N))
        elif technique.technique_type == TechniqueType.DEAL:
            func.compose(LinearFunc(technique.N, 0))
    return func
  

def get_final_position_of_card(card_num, num_cards, shuffle):
    func = get_linear_func(shuffle)
    func.reduce(num_cards)
    return func.evaluate(card_num) % num_cards
    
    
def get_final_card_at_position(position, num_cards, shuffle, num_shuffles):
    func = get_linear_func(shuffle)
    func.reduce(num_cards)
    func.repeat_and_reduce(num_shuffles, num_cards)
    return func.evaluate_inverse(position, num_cards)
  
        
def parse_lines(lines):
    shuffle = []
    for line in lines:
        if 'new' in line:
            shuffle.append(Technique(TechniqueType.NEW))
        elif 'increment' in line:
            N = int(line.split()[-1])
            shuffle.append(Technique(TechniqueType.DEAL, N))
        elif 'cut' in line:
            N = int(line.split()[-1])
            shuffle.append(Technique(TechniqueType.CUT, N))
        else:
            raise ValueError('Invalid line to parse')
    return shuffle
            

def main():
    with open('input22.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        shuffle = parse_lines(lines)
        
    # Part 1
    print(get_final_position_of_card(CARD_OF_INTEREST, TOTAL_CARDS_PART1, shuffle))
    
    # Part 2
    print(get_final_card_at_position(POSITION_OF_INTEREST, TOTAL_CARDS_PART2, shuffle, NUM_SHUFFLES))
    
    
if __name__ == '__main__':
    main()
