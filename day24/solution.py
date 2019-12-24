import unittest

DATA = '''
    .##.#
    ###..
    #...#
    ##.#.
    .###.
'''.strip(' \n').replace(' ', '')


class TestGold(unittest.TestCase):
    EXAMPLE_0 = '''
        ....#
        #..#.
        #..##
        ..#..
        #....
    '''.strip(' \n').replace(' ', '')


    def test_code_decode(self):
        self.assertEqual(
            self.EXAMPLE_0,
            decode_world(encode_world(self.EXAMPLE_0))
        )

    def test_neighbours_19(self):
        self.assertSetEqual(
            {(3, 4, 0), (4, 3, 0), (2, 3, 0), (3, 2, 0)},
            generate_neighbouring_locations((3, 3, 0))
        )

    def test_neighbours_G(self):
        self.assertSetEqual(
            {(1, 0, -1), (0, 1, -1), (2, 1, -1), (1, 2, -1)},
            generate_neighbouring_locations((1, 1, -1))
        )

    def test_neighbours_D(self):
        self.assertSetEqual(
            {(2, 1, 0), (2, 0, -1), (4, 0, -1), (3, 1, -1)},
            generate_neighbouring_locations((3, 0, -1))
        )

    def test_neighbours_E(self):
        self.assertSetEqual(
            {(2, 1, 0), (3, 0, -1), (3, 2, 0), (4, 1, -1)},
            generate_neighbouring_locations((4, 0, -1))
        )

    def test_neighbours_14(self):
        self.assertSetEqual(
            {(3, 1, 0), (4, 0, -1), (4, 1, -1), (4, 2, -1), (4, 3, -1), (4, 4, -1), (4, 2, 0), (3, 3, 0)},
            generate_neighbouring_locations((3, 2, 0))
        )

    def test_example_0_tick(self):
        bugs = encode_world(self.EXAMPLE_0)
        bugs = multi_tick(bugs, 10)
        self.assertEqual(
            99,
            len(bugs)
        )

    def test_assignement(self):
        self.assertEqual(
            1953,
            len(multi_tick(encode_world(DATA), 200))
        )


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


def solve_gold(world):
    history = [encode_world(world)]
    while history[-1] not in history[:-1]:
        history.append(tick(history[-1]))
    return len(history[-1])


def biodiversity_rating(bugs):
    world = decode_world(bugs).replace('\n', '')
    return sum(
        2 ** i
        for i, char in enumerate(world)
        if char == '#'
    )


def multi_tick(bugs, i):
    for _ in range(i):
        bugs = tick(bugs)
    return bugs


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
    neighbours = {
        (location[0] + delta_x, location[1] + delta_y, location[2])
        for delta_x in (-1, 0, 1)
        for delta_y in (-1, 0, 1)
        if (
                abs(delta_x) + abs(delta_y) == 1
                and
                0 <= location[0] + delta_x <= 4
                and
                0 <= location[1] + delta_y <= 4
                and
                (location[0] + delta_x, location[1] + delta_y) != (2, 2)
        )
    }

    # deeper
    for case, inner_neighbours in (
            ((1, 2), {(0, i, location[2] - 1) for i in range(5)}),
            ((2, 1), {(i, 0, location[2] - 1) for i in range(5)}),
            ((3, 2), {(4, i, location[2] - 1) for i in range(5)}),
            ((2, 3), {(i, 4, location[2] - 1) for i in range(5)}),
    ):
        if (location[0], location[1]) == case:
            neighbours = neighbours.union(inner_neighbours)

    # more at the surface
    if location[0] == 0:
        neighbours.add((1, 2, location[2] + 1))
    if location[0] == 4:
        neighbours.add((3, 2, location[2] + 1))
    if location[1] == 0:
        neighbours.add((2, 1, location[2] + 1))
    if location[1] == 4:
        neighbours.add((2, 3, location[2] + 1))

    return neighbours
