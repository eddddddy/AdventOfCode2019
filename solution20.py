from solution18 import Direction, Position


class Donut:
    def __init__(self, donut):
        self.donut = donut

    def __getitem__(self, item):
        return self.donut[item.position[0]][item.position[1]]

    def is_inner(self, position):
        try:
            if position.position[0] < 3 or position.position[1] < 3:
                return False
            self.donut[position.position[0]][position.position[1] + 3]
            self.donut[position.position[0] + 3][position.position[1]]
            return True
        except IndexError:
            return False


OPEN = '.'
WALL = '#'
SPACE = ' '
START = 'AA'
END = 'ZZ'
directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


def find_shortest_path(donut, portals, start, end):
    seen = set()
    to_explore = [(start, 0)]

    while to_explore:
        point_to_explore, path_length = to_explore[0]
        for direction in directions:
            stepped = point_to_explore.step(direction)

            if stepped in seen or donut[stepped] == WALL:
                continue

            seen.add(stepped)

            if stepped in portals:
                stepped = portals[stepped]
                seen.add(stepped)

            if stepped == end:
                return path_length + 1

            to_explore.append((stepped, path_length + 1))

        seen.add(point_to_explore)
        to_explore = to_explore[1:]


def find_shortest_path_with_depth(donut, portals, start, end):
    seen = set()
    to_explore = [(start, 0, 0)]

    while to_explore:
        point_to_explore, path_length, level = to_explore[0]

        for direction in directions:
            new_level = level
            stepped = point_to_explore.step(direction)

            if (stepped, level) in seen or donut[stepped] == WALL:
                continue

            seen.add((stepped, level))

            if stepped in portals:
                if donut.is_inner(stepped):
                    new_level += 1
                else:
                    if new_level == 0:
                        continue
                    elif stepped == start or stepped == end:
                        continue
                    new_level -= 1

                stepped = portals[stepped]
                if (stepped, new_level) in seen:
                    continue
                seen.add((stepped, new_level))

            if stepped == end:
                if new_level == 0:
                    return path_length + 1

            to_explore.append((stepped, path_length + 1, new_level))

        seen.add((point_to_explore, level))
        to_explore = to_explore[1:]


def parse_donut(raw_donut):
    unclaimed_portals = {}
    portals = {}
    start = None
    end = None

    for i, row in enumerate(raw_donut):
        for j, tile in enumerate(row):
            if not tile.isupper():
                continue

            if row[j + 1].isupper():
                try:
                    if row[j + 2] == OPEN:
                        pid = tile + row[j + 1]
                        enter = Position(i, j + 1)
                        landing = Position(i, j + 2)
                        extra = (i, j)
                    else:
                        raise IndexError
                except IndexError:
                    pid = tile + row[j + 1]
                    enter = Position(i, j)
                    landing = Position(i, j - 1)
                    extra = (i, j + 1)
            elif raw_donut[i + 1][j].isupper():
                try:
                    if raw_donut[i + 2][j] == OPEN:
                        pid = tile + raw_donut[i + 1][j]
                        enter = Position(i + 1, j)
                        landing = Position(i + 2, j)
                        extra = (i, j)
                    else:
                        raise IndexError
                except IndexError:
                    pid = tile + raw_donut[i + 1][j]
                    enter = Position(i, j)
                    landing = Position(i - 1, j)
                    extra = (i + 1, j)

            if pid == START or pid == END:
                raw_donut[extra[0]][extra[1]] = SPACE
                raw_donut[enter.position[0]][enter.position[1]] = WALL
                if pid == START:
                    start = landing
                else:
                    end = landing
                continue

            raw_donut[extra[0]][extra[1]] = SPACE
            raw_donut[enter.position[0]][enter.position[1]] = OPEN

            if pid in unclaimed_portals:
                other = unclaimed_portals.pop(pid)
                portals[enter] = other[1]
                portals[other[0]] = landing
            else:
                unclaimed_portals[pid] = (enter, landing)

    assert not unclaimed_portals and start and end
    return Donut(raw_donut), portals, start, end


def main():
    with open('input20.txt', 'r') as f:
        raw_donut = [list(line.rstrip('\n')) for line in f.readlines()]
        donut, portals, start, end = parse_donut(raw_donut)

    # Part 1
    print(find_shortest_path(donut, portals, start, end))

    # Part 2
    print(find_shortest_path_with_depth(donut, portals, start, end))


if __name__ == '__main__':
    main()
