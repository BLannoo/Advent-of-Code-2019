from math import sqrt, pi
from typing import Tuple, Set
from unittest import TestCase

import pandas as pd
from numpy.ma import arccos


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


def dist(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# cosine rule: https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
def angle_from_up(target, corner=(0, 0)):
    reference = (corner[0], corner[1] - 1)
    p1 = corner
    p2 = reference
    p3 = target
    p12 = dist(p1, p2)
    p13 = dist(p1, p3)
    p23 = dist(p2, p3)
    radials = arccos((p12 ** 2 + p13 ** 2 - p23 ** 2) / (2 * p12 * p13))
    angle = radials * 180 / pi
    if target[0] < reference[0]:
        angle = 360 - angle
    return angle


def solve_gold(field, station):
    field.remove(station)
    df = pd.DataFrame(field, columns=['x', 'y'])
    df['angle'] = df.apply(
        lambda row: round(
            angle_from_up((row.x, row.y), corner=station)
            , 5
        ),
        axis=1
    )
    df['distance'] = df.apply(
        lambda row: round(dist(station, (row.x, row.y)), 5),
        axis=1
    )
    df.sort_values(['angle', 'distance'], inplace=True)
    asteroid_200 = df.groupby(by='angle').first().iloc[199]
    return asteroid_200


class TestGold(TestCase):
    def test_example_a(self):
        self.assertEqual(angle_from_up((0, -1)), 0)
        self.assertAlmostEqual(angle_from_up((1, -1)), 45)
        self.assertAlmostEqual(angle_from_up((1, 0)), 90)
        self.assertAlmostEqual(angle_from_up((1, 1)), 135)
        self.assertAlmostEqual(angle_from_up((0, 1)), 180)
        self.assertAlmostEqual(angle_from_up((-1, 1)), 225)
        self.assertAlmostEqual(angle_from_up((-1, 0)), 270)
        self.assertAlmostEqual(angle_from_up((-1, -1)), 315)
        self.assertAlmostEqual(angle_from_up((0, -1)), 0)

    def test_example_0(self):
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

        asteroid_200 = solve_gold(field, station=(11, 13))
        self.assertEqual(
            (asteroid_200.x, asteroid_200.y),
            (8, 2)
        )

    def test_assignement(self):
        with open('data.txt') as file:
            data = ''.join(file.readlines())
        field = generate(data)

        asteroid_200 = solve_gold(field, station=(20, 21))
        self.assertEqual(
            (asteroid_200.x, asteroid_200.y),
            (19, 19)
        )
