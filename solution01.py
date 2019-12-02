def calculate_fuel(mass):
    return mass // 3 - 2


def calculate_fuel_recursive(mass):
    subtotal = calculate_fuel(mass)
    if subtotal <= 0:
        return 0
    else:
        return subtotal + calculate_fuel_recursive(subtotal)


def calculate_fuel_all():
    with open('input01.txt') as f:
        masses = [int(line) for line in f.readlines()]
        fuel_required = [calculate_fuel(mass) for mass in masses]
        return sum(fuel_required)


def calculate_fuel_recursive_all():
    with open('input01.txt') as f:
        masses = [int(line) for line in f.readlines()]
        fuel_required = [calculate_fuel_recursive(mass) for mass in masses]
        return sum(fuel_required)


def main():
    # Part 1
    print(calculate_fuel_all())

    # Part 2
    print(calculate_fuel_recursive_all())


if __name__ == '__main__':
    main()
