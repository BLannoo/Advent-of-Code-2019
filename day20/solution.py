from typing import List, Tuple, Set
from unittest import TestCase

import numpy as np


def read_labyrinth(file_name: str):
    map = []
    with open(file_name) as file:
        for line in file:
            map.append(list(line.replace(' ', '#').replace('\n', '')))
    map = np.array(map)
    return map


def print_map(map, highlight: List[Tuple[int, int]] = []):
    YELLOW = '\033[93m'
    WHITE = '\033[0m'
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if (i, j) in highlight:
                print(YELLOW + map[i, j] + WHITE, end='')
            else:
                print(map[i, j], end='')
        print()


def find_portals(name: str, map) -> Set[Tuple[int, int]]:
    entrances = set()
    first_letter_options = tuple(zip(*np.nonzero(map == name[0])))
    for (x_1, y_1) in first_letter_options:
        for (x_dir, y_dir) in [(1, 0), (0, 1)]:
            x_2 = x_1 + x_dir
            y_2 = y_1 + y_dir
            if map[x_2, y_2] == name[1]:
                x_further = x_2 + x_dir
                y_further = y_2 + y_dir
                x_back = x_1 - x_dir
                y_back = y_1 - y_dir
                if map[x_further, y_further] == '.':
                    entrances.add((x_further, y_further))
                elif map[x_back, y_back] == '.':
                    entrances.add((x_back, y_back))
                else:
                    raise Exception("portal '{}' not next to entrance".format(name))
    return entrances


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def read_portal(location: Tuple[int, int], map) -> str:
    original_letter = map[location]

    second_letter = map[location[0] + 1, location[1]]
    if second_letter in ALPHABET:
        return original_letter + second_letter
    second_letter = map[location[0], location[1] + 1]
    if second_letter in ALPHABET:
        return original_letter + second_letter

    first_letter = map[location[0] - 1, location[1]]
    if first_letter in ALPHABET:
        return first_letter + original_letter
    first_letter = map[location[0], location[1] - 1]
    if first_letter in ALPHABET:
        return first_letter + original_letter


DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def movement_options(location: Tuple[int, int], map) -> Set[Tuple[int, int]]:
    options = set()
    for dx, dy in DIRECTIONS:
        option = location[0] + dx, location[1] + dy
        if map[option] == '.':
            options.add(option)
        elif map[option] in ALPHABET:
            portals = find_portals(read_portal(option, map), map)
            portals.remove(location)
            if len(portals) == 1:
                options.add(portals.pop())
    return options


def is_finish(location: Tuple[int, int], map) -> bool:
    for dx, dy in DIRECTIONS:
        if read_portal((location[0] + dx, location[1] + dy), map) == 'ZZ':
            return True
    return False


def breadth_first(start_location, map):
    paths = [[start_location]]
    while not is_finish(paths[0][-1], map):
        path = paths[0]
        options = movement_options(path[-1], map)
        for option in options:
            if option not in path:
                new_path = path.copy()
                new_path.append(option)
                paths.append(new_path)
        paths.remove(path)
    return paths


def solve_silver(temp):
    map = read_labyrinth(temp)
    start_location = find_portals('AA', map).pop()
    paths = breadth_first(start_location, map)
    print_map(map, highlight=paths[0])
    silver = len(paths[0]) - 1
    return silver


class TestSilver(TestCase):
    def test_find_portal(self):
        map = read_labyrinth('example0.txt')
        self.assertSetEqual(
            {(3, 10)},
            find_portals('AA', map)
        )
        self.assertSetEqual(
            {(7, 10), (9, 3)},
            find_portals('BC', map)
        )

    def test_read_portal(self):
        map = read_labyrinth('example0.txt')
        self.assertEqual(
            'AA',
            read_portal((2, 10), map)
        )
        self.assertEqual(
            'BC',
            read_portal((8, 10), map)
        )
        self.assertEqual(
            'BC',
            read_portal((9, 2), map)
        )
        self.assertEqual(
            'ZZ',
            read_portal((18, 14), map)
        )

    def test_movement_options(self):
        map = read_labyrinth('example0.txt')
        self.assertSetEqual(
            {(4, 10)},
            movement_options((3, 10), map)
        )
        self.assertSetEqual(
            {(3, 10), (5, 10), (4, 11)},
            movement_options((4, 10), map)
        )
        self.assertSetEqual(
            {(6, 10), (9, 3)},
            movement_options((7, 10), map)
        )

    def test_is_finish(self):
        map = read_labyrinth('example0.txt')

        self.assertTrue(
            is_finish((17, 14), map)
        )
        self.assertFalse(
            is_finish((3, 10), map)
        )
        self.assertFalse(
            is_finish((4, 10), map)
        )

    def test_example0(self):
        self.assertEqual(
            23,
            solve_silver('example0.txt')
        )

    def test_example1(self):
        self.assertEqual(
            58,
            solve_silver('example1.txt')
        )

    def test_assignement(self):
        self.assertEqual(
            570,
            solve_silver('data.txt')
        )
