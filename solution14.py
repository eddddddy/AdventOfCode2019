fuel = 'FUEL'
ore = 'ORE'

key_amount = 'amount'

NUM_ORES_IN_CARGO = 1000000000000


def update_required_and_excess(chemical, amount, excess):
    if chemical in excess:
        if amount >= excess[chemical]:
            return amount - excess.pop(chemical)
        else:
            excess[chemical] -= amount
            return 0
    else:
        return amount


def get_ores_required(reactions, chemical, amount, excess):
    reaction = reactions[chemical]
    required_amount = update_required_and_excess(chemical, amount, excess)
    num_reactions_required = ((required_amount // reaction[key_amount]) +
                              (required_amount % reaction[key_amount] > 0))

    excess_chemical = num_reactions_required * reaction[key_amount] - required_amount
    if excess_chemical > 0:
        excess[chemical] = excess_chemical

    if len(reaction) == 2 and ore in reaction:
        return num_reactions_required * reaction[ore]

    ore_subtotal = 0
    for sub_chemical in reaction:
        if sub_chemical == key_amount:
            continue
        ore_subtotal += get_ores_required(reactions,
                                          sub_chemical,
                                          reaction[sub_chemical] * num_reactions_required,
                                          excess)

    return ore_subtotal


def get_ores_required_for_fuel(reactions):
    return get_ores_required(reactions, fuel, 1, {})


def get_fuel_produced_from_ore(reactions, num_ores):
    curr = 1
    while get_ores_required(reactions, fuel, curr, {}) < num_ores:
        curr *= 2

    lower = curr // 2
    upper = curr
    curr = curr // 2

    while True:
        ores_required = get_ores_required(reactions, fuel, curr, {})

        if lower + 1 == upper:
            return lower

        if ores_required < num_ores:
            lower = curr
            curr = (curr + upper) // 2
        else:
            upper = curr
            curr = (curr + lower) // 2


def parse_reaction(reaction_str):
    reactants = reaction_str.split('=')[0].strip().split(',')
    product = reaction_str.split('>')[1].strip()

    reaction = {}
    product_amount, product_name = product.split()
    reaction[key_amount] = int(product_amount)

    for reactant in reactants:
        reactant_amount, reactant_name = reactant.split()
        reaction[reactant_name] = int(reactant_amount)

    return product_name, reaction


def main():
    with open('input14.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        reactions = [parse_reaction(line) for line in lines]
        reactions = {product_name: reaction for product_name, reaction in reactions}

    # Part 1
    print(get_ores_required_for_fuel(reactions))

    # Part 2
    print(get_fuel_produced_from_ore(reactions, NUM_ORES_IN_CARGO))


if __name__ == '__main__':
    main()
