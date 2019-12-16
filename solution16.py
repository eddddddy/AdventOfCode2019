import numpy as np

NUM_PHASES = 100
NUM_DIGITS = 8
REAL_SIGNAL_REPETITION = 10000


def get_convolution_matrix(signal_length):
    base_pattern = [0, 1, 0, -1]
    convolution = []
    for i in range(1, signal_length + 1):
        pattern = [q for p in base_pattern for q in [p] * i]
        pattern *= (signal_length // len(pattern) + 1)
        pattern = pattern[1: signal_length + 1]
        convolution.append(pattern)
    return np.array(convolution)


def run_fft(num_phases, signal):
    signal = np.array(signal)
    convolution_matrix = get_convolution_matrix(len(signal))
    for _ in range(num_phases):
        signal = np.mod(np.abs(convolution_matrix @ signal), 10)
    return signal


def get_real_message(signal, num_phases, num_repetitions):
    total_length = len(signal) * num_repetitions
    offset = int("".join(map(str, signal[:7])))
    vec = np.zeros(total_length - offset, dtype=np.int32)
    curr_binomial = 1

    for diff in range(total_length - offset):
        curr_binomial = curr_binomial * (num_phases + diff - 1) // diff if diff > 0 else 1
        f = curr_binomial % 10
        vec[diff] = f

    signal = (signal * 10000)[offset:]

    real = np.zeros(NUM_DIGITS, dtype=np.int32)
    for i in range(NUM_DIGITS):
        real[i] = (vec @ signal) % 10
        vec = np.roll(vec, 1)
        vec[0] = 0

    return real


def main():
    with open('input16.txt') as f:
        signal = [int(c) for c in f.readline().strip()]

    # Part 1
    print(''.join(map(str, run_fft(NUM_PHASES, signal)[:NUM_DIGITS])))

    # Part 2
    print(''.join(map(str, get_real_message(signal, NUM_PHASES, REAL_SIGNAL_REPETITION))))


if __name__ == '__main__':
    main()
