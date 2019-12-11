from typing import Tuple, Set
from unittest import TestCase


def generate(pattern) -> Set[Tuple[int, int]]:
    split = pattern.strip('\n').split('\n')
    return {
        (j, i)
        for i in range(len(split))
        for j in range(len(split[0]))
        if split[i][j] == '#'
    }


def hiding(position, asteroid, field):
    dx = asteroid[0] - position[0]
    dy = asteroid[1] - position[1]
    for nominator in range(1, 20):
        for denominator in range(1, nominator):
            dx_fraction = dx * denominator / nominator
            dy_fraction = dy * denominator / nominator
            if (position[0] + dx_fraction, position[1] + dy_fraction) in field:
                return True


def line_of_sight(position: Tuple[int, int], field: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    return {
        asteroid
        for asteroid in field.difference({position})
        if not hiding(position, asteroid, field)
    }


def best_location(field):
    return max([
        (asteroid, len(line_of_sight(asteroid, field)))
        for asteroid in field
    ], key=lambda a: a[1])


class TestSilver(TestCase):
    def test_example_0(self):
        field = generate('''
            .#..#
            .....
            #####
            ....#
            ...##
        '''.replace(' ', ''))

        self.assertEqual(
            {(4, 0), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4)},
            line_of_sight((3, 4), field)
        )
        self.assertEqual(
            {(1, 2), (3, 2), (4, 4), (4, 3), (1, 0), (3, 4), (4, 0)},
            line_of_sight((2, 2), field)
        )
        self.assertEqual(
            ((3, 4), 8),
            best_location(field)
        )

    def test_example_1(self):
        field = generate('''
            ......#.#.
            #..#.#....
            ..#######.
            .#.#.###..
            .#..#.....
            ..#....#.#
            #..#....#.
            .##.#..###
            ##...#..#.
            .#....####
        '''.replace(' ', ''))

        self.assertEqual(
            ((5, 8), 33),
            best_location(field)
        )

    def test_example_4(self):
        field = generate('''
            .#..##.###...#######
            ##.############..##.
            .#.######.########.#
            .###.#######.####.#.
            #####.##.#.##.###.##
            ..#####..#.#########
            ####################
            #.####....###.#.#.##
            ##.#################
            #####.##.###..####..
            ..######..##.#######
            ####.##.####...##..#
            .#####..#.######.###
            ##...#.##########...
            #.##########.#######
            .####.#.###.###.#.##
            ....##.##.###..#####
            .#.#.###########.###
            #.#.#.#####.####.###
            ###.##.####.##.#..##
        '''.replace(' ', ''))

        self.assertEqual(
            ((11, 13), 210),
            best_location(field)
        )

    # 15 -> 252 is to high
    # 20 -> 247
    def test_assignement(self):
        with open('data.txt') as file:
            data = ''.join(file.readlines())
        field = generate(data)
        self.assertEqual(
            ((20, 21), 247),
            best_location(field)
        )
