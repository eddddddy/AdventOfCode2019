from functools import reduce

import numpy as np

width = 25
height = 6


def main_part1(data):
    data = np.array(data).reshape((-1, height, width))

    min_zeros = width * height + 1
    min_layer = None
    for layer in data:
        num_zeros = np.count_nonzero(layer == 0)
        if num_zeros < min_zeros:
            min_zeros = num_zeros
            min_layer = layer

    return np.count_nonzero(min_layer == 1) * np.count_nonzero(min_layer == 2)


def encode_pixel(p):
    if p == 0:
        return 999999
    elif p == 1:
        return -999999
    elif p == 2:
        return 0
    else:
        return p


def decode_pixel(p):
    if p == 0:
        return 0
    elif p == 1:
        return 1
    elif p > 0:
        return 0
    else:
        return 1


def stack_layers(layer1, layer2):
    layer1 = np.vectorize(encode_pixel)(layer1)
    return layer1 + layer2


def prettify(pixels):
    pixels = list(pixels)
    pretty_pixels = [['#' if p == 1 else ' ' for p in row] for row in pixels]
    return '\n'.join([''.join(row) for row in pretty_pixels])


def main_part2(data):
    data = np.array(data).reshape((-1, height, width))
    return np.vectorize(decode_pixel)(reduce(stack_layers, data))


def main():
    with open('input08.txt') as f:
        data = [int(p) for p in f.readline().strip()]

    # Part 1
    print(main_part1(data))

    # Part 2
    print(prettify(main_part2(data)))


if __name__ == '__main__':
    main()
