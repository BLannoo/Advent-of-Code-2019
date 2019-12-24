import unittest


def encode_world(world):
    bugs = set()
    for i in range(5):
        for j in range(5):
            if world[i + 6 * j] == '#':
                bugs.add((i, j, 0))
    return bugs


def decode_world(bugs):
    world = ''
    for i in range(5):
        for j in range(5):
            if (j, i, 0) in bugs:
                world += '#'
            else:
                world += '.'
        world += '\n'
    return world[:-1]


def biodiversity_rating(bugs):
    world = decode_world(bugs).replace('\n', '')
    return sum(
        2 ** i
        for i, char in enumerate(world)
        if char == '#'
    )


def solve_silver(world):
    history = [encode_world(world)]
    while history[-1] not in history[:-1]:
        history.append(tick(history[-1]))
    return biodiversity_rating(history[-1])


class TestSilver(unittest.TestCase):
    EXAMPLE_0 = '''
        ....#
        #..#.
        #..##
        ..#..
        #....
    '''.strip(' \n').replace(' ', '')

    EXAMPLE_1 = '''
        #..#.
        ####.
        ###.#
        ##.##
        .##..
    '''.strip(' \n').replace(' ', '')

    def test_code_decode(self):
        self.assertEqual(
            self.EXAMPLE_0,
            decode_world(encode_world(self.EXAMPLE_0))
        )

    def test_example_0_tick(self):
        bugs = encode_world(self.EXAMPLE_0)
        bugs = tick(bugs)
        self.assertEqual(
            self.EXAMPLE_1,
            decode_world(bugs)
        )

    def test_example_0(self):
        self.assertEqual(
            2129920,
            solve_silver(self.EXAMPLE_0)
        )

    DATA = '''
        .##.#
        ###..
        #...#
        ##.#.
        .###.
    '''.strip(' \n').replace(' ', '')

    def test_assignement(self):
        self.assertEqual(
            1151290,
            solve_silver(self.DATA)
        )


def tick(old_universe):
    new_universe = apply_rules(old_universe)
    return {
        cell
        for cell in potential_living_cells(old_universe)
        if new_universe(cell)
    }


def apply_rules(old_universe):
    def new_universe(location):
        neighbouring_locations = generate_neighbouring_locations(location)
        number_of_living_neighbours = len(neighbouring_locations.intersection(old_universe))
        return (
                (number_of_living_neighbours == 1 and location in old_universe)
                or
                (number_of_living_neighbours in (1, 2) and location not in old_universe)
        )

    return new_universe


def potential_living_cells(old_universe):
    return {
        position
        for living_cell in old_universe
        for position in generate_neighbouring_locations(living_cell)
    }.union(old_universe)


def generate_neighbouring_locations(location):
    return {
        (location[0] + delta_x, location[1] + delta_y, location[2])
        for delta_x in (-1, 0, 1)
        for delta_y in (-1, 0, 1)
        if (
                abs(delta_x) + abs(delta_y) == 1
                and
                0 <= location[0] + delta_x <= 4
                and
                0 <= location[1] + delta_y <= 4
        )
    }
