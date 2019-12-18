from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Position:
    def __init__(self, i, j):
        self.position = (i, j)

    def __repr__(self):
        return f'({self.position[0]}, {self.position[1]})'

    def __hash__(self):
        return hash(self.position)

    def __eq__(self, other):
        return self.position == other.position

    def step(self, direction):
        return {
            Direction.UP: Position(self.position[0] - 1, self.position[1]),
            Direction.DOWN: Position(self.position[0] + 1, self.position[1]),
            Direction.LEFT: Position(self.position[0], self.position[1] - 1),
            Direction.RIGHT: Position(self.position[0], self.position[1] + 1)
        }[direction]


class Vault:
    def __init__(self, vault):
        self.vault = vault

    def __getitem__(self, item):
        if item.position[0] >= len(self.vault) or item.position[0] < 0:
            raise IndexError
        elif item.position[1] >= len(self.vault[0]) or item.position[1] < 0:
            raise IndexError
        return self.vault[item.position[0]][item.position[1]]

    def get_player_positions(self):
        player_positions = []
        for i, row in enumerate(self.vault):
            for j, tile in enumerate(row):
                if tile == ENTRANCE:
                    player_positions.append(Position(i, j))
        return player_positions

    def get_key_positions(self):
        key_positions = {}
        for i, row in enumerate(self.vault):
            for j, tile in enumerate(row):
                if tile.islower():
                    key_positions[tile] = Position(i, j)
        return key_positions

    def partition(self):
        for i, row in enumerate(self.vault):
            for j, tile in enumerate(row):
                if tile == ENTRANCE:
                    row[j - 1] = WALL
                    row[j] = WALL
                    row[j + 1] = WALL

                    row_above = self.vault[i - 1]
                    row_above[j - 1] = ENTRANCE
                    row_above[j] = WALL
                    row_above[j + 1] = ENTRANCE
                    self.vault[i - 1] = row_above

                    row_below = self.vault[i + 1]
                    row_below[j - 1] = ENTRANCE
                    row_below[j] = WALL
                    row_below[j + 1] = ENTRANCE
                    self.vault[i + 1] = row_below

                    return


OPEN = '.'
WALL = '#'
ENTRANCE = '@'
directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
INT_MAX = 999999


def shortest_paths_to_key(vault, start_positions, key_positions):
    path_lengths_and_keys_required = {}

    for i, start_position in enumerate(start_positions):
        seen = set()
        to_explore = [(start_position, [], 0)]

        while to_explore:
            point_to_explore, keys_required, num_steps = to_explore[0]
            for direction in directions:
                try:
                    stepped = point_to_explore.step(direction)
                except IndexError:
                    continue

                if stepped in seen or vault[stepped] == WALL:
                    continue

                if vault[stepped].isupper():
                    new_keys_required = keys_required + [vault[stepped].lower()]
                else:
                    new_keys_required = keys_required

                if stepped in key_positions:
                    path_lengths_and_keys_required[key_positions[stepped]] = (num_steps + 1, new_keys_required, i)

                to_explore.append((stepped, new_keys_required, num_steps + 1))
                seen.add(stepped)

            seen.add(point_to_explore)
            to_explore = to_explore[1:]

    return path_lengths_and_keys_required


def find_all_keys_rec(vault, positions, key_positions, inventory, shortest_path_memo, path_lengths_to_keys_memo):
    keys_to_find = set(key_positions.keys()) - inventory

    if (tuple(positions), tuple(inventory)) in shortest_path_memo:
        return shortest_path_memo[(tuple(positions), tuple(inventory))]

    if not keys_to_find:
        return 0

    shortest_path_so_far = INT_MAX
    if tuple(positions) in path_lengths_to_keys_memo:
        path_lengths_to_keys = path_lengths_to_keys_memo[tuple(positions)]
    else:
        path_lengths_to_keys = shortest_paths_to_key(vault, positions, {v: k for k, v in key_positions.items()})
        path_lengths_to_keys_memo[tuple(positions)] = path_lengths_to_keys

    for key in keys_to_find:
        path_length, keys_required, index = path_lengths_to_keys[key]
        if set(keys_required) - inventory:
            continue

        new_start_positions = [key_positions[key] if i == index else position for i, position in enumerate(positions)]
        remaining_path = find_all_keys_rec(vault, new_start_positions, key_positions, inventory | set(key),
                                           shortest_path_memo, path_lengths_to_keys_memo)
        if path_length + remaining_path < shortest_path_so_far:
            shortest_path_so_far = path_length + remaining_path

    shortest_path_memo[(tuple(positions), tuple(inventory))] = shortest_path_so_far
    return shortest_path_so_far


def find_all_keys(vault):
    return find_all_keys_rec(vault, vault.get_player_positions(), vault.get_key_positions(), set(), {}, {})


def main():
    with open('input18.txt') as f:
        vault = [list(line.strip()) for line in f.readlines()]
        vault = Vault(vault)

    # Part 1
    print(find_all_keys(vault))

    vault.partition()

    # Part 2
    print(find_all_keys(vault))


if __name__ == '__main__':
    main()
