from unittest import TestCase


def load_data():
    with open('data.txt') as file:
        return [
            orbit_pair.strip('\n').split(')')
            for orbit_pair in file
        ]


def solve_silver(data):
    return sum(
        len(orbits(orbit_pair[1], data)) - 1
        for orbit_pair in data
    )


def solve_gold(data):
    orbits_san = orbits('SAN', data)
    orbits_you = orbits('YOU', data)
    # -2 = - SAN - YOU - 1 edge less then nodes + symmetric difference removes the switching planet
    return len(orbits_san.symmetric_difference(orbits_you)) - 2


def orbits(planet, data):
    orbit_chain = {planet}
    while planet != 'COM':
        planet = next(
            orbit_pair
            for orbit_pair in data
            if orbit_pair[1] == planet
        )[0]
        orbit_chain.add(planet)
    return orbit_chain


class TestSilver(TestCase):
    def test_example_a(self):
        self.assertEqual(
            1,
            solve_silver([('COM', 'A')])
        )

    def test_example_b(self):
        self.assertEqual(
            3,
            solve_silver([('COM', 'A'), ('A', 'B')])
        )

    def test_example_c(self):
        self.assertEqual(
            2,
            solve_silver([('COM', 'A'), ('COM', 'B')])
        )

    def test_example_d(self):
        self.assertEqual(
            6,
            solve_silver([('COM', 'A'), ('A', 'B'), ('B', 'C')])
        )

    def test_example_0(self):
        self.assertEqual(
            42,
            solve_silver(
                [
                    orbit_pair.split(')')
                    for orbit_pair in 'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L'.split(',')
                ]
            )
        )

    def test_assignement(self):
        self.assertEqual(
            171213,
            solve_silver(load_data())
        )


class TestGold(TestCase):
    def test_example_0(self):
        data = [
            orbit_pair.split(')')
            for orbit_pair in 'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L,K)YOU,I)SAN'.split(',')
        ]
        self.assertEqual(
            4,
            solve_gold(data)
        )

    def test_assignment(self):
        self.assertEqual(
            292,
            solve_gold(load_data())
        )
