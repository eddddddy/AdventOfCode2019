def is_non_decreasing(num_str):
    return list(num_str) == sorted(num_str)


def is_valid(num_str):
    if len(num_str) != 6:
        return False

    if not is_non_decreasing(num_str):
        return False

    digit_counts = map(lambda n: num_str.count(str(n)), range(10))
    return len(list(filter(lambda count: count >= 2, digit_counts))) > 0


def is_valid2(num_str):
    if len(num_str) != 6:
        return False

    if not is_non_decreasing(num_str):
        return False

    digit_counts = map(lambda n: num_str.count(str(n)), range(10))
    return 2 in list(digit_counts)


def count_valid_passwords():
    with open('input04.txt') as f:
        start, end = f.readline().split('-')
        start, end = int(start), int(end)
        return len(list(filter(lambda num: is_valid(str(num)), range(start, end + 1))))


def count_valid_passwords2():
    with open('input04.txt') as f:
        start, end = f.readline().split('-')
        start, end = int(start), int(end)
        return len(list(filter(lambda num: is_valid2(str(num)), range(start, end + 1))))


def main():
    # Part 1
    print(count_valid_passwords())

    # Part 2
    print(count_valid_passwords2())


if __name__ == '__main__':
    main()
