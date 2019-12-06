from typing import List, Dict, Union

center = 'COM'
you = 'YOU'
santa = 'SAN'


def get_orbit_info(orbit_pairs: List[List[str]]) -> Dict[str, List[Union[str, List[str]]]]:
    orbit_info = {center: ['', []]}
    for pair in orbit_pairs:
        orbitee, orbiter = pair

        if orbitee not in orbit_info:
            orbit_info[orbitee] = ['', []]

        if orbiter not in orbit_info:
            orbit_info[orbiter] = ['', []]

        orbit_info[orbitee][1].append(orbiter)
        orbit_info[orbiter][0] = orbitee

    return orbit_info


def get_orbits_rec(orbit_info, root, accum=0):
    orbiters = orbit_info[root][1]

    if not orbiters:
        return accum

    total = accum
    for orbiter in orbiters:
        total += get_orbits_rec(orbit_info, orbiter, accum + 1)

    return total


def get_total_orbits():
    with open('input06.txt') as f:
        orbits = [line.strip().split(')') for line in f.readlines()]
        orbit_info = get_orbit_info(orbits)
        return get_orbits_rec(orbit_info, center)


def get_steps_to_santa(orbit_info):
    start = orbit_info[you][0]
    end = orbit_info[santa][0]

    steps = 0
    you_steps = {}
    current = start
    while current != center:
        you_steps[current] = steps
        current = orbit_info[current][0]
        steps += 1

    current = end
    steps = 0
    while current != center:
        if current in you_steps:
            return you_steps[current] + steps
        current = orbit_info[current][0]
        steps += 1


def main_part2():
    with open('input06.txt') as f:
        orbits = [line.strip().split(')') for line in f.readlines()]
        orbit_info = get_orbit_info(orbits)
        return get_steps_to_santa(orbit_info)


def main():
    # Part 1
    print(get_total_orbits())

    # Part 2
    print(main_part2())


if __name__ == '__main__':
    main()
