from itertools import permutations
from typing import Tuple, Set, List, Dict
from unittest import TestCase

import numpy as np

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))


class Segment:
    def __init__(self, length: int, dependencies: Set[str]):
        self.length = length
        self.dependencies = dependencies

    def __eq__(self, other: 'Segment') -> bool:
        return self.length == other.length and self.dependencies == other.dependencies

    def __repr__(self) -> str:
        return f'Segment(length={self.length}, dependencies={self.dependencies})'


def is_valid(path: Tuple, all_segments: Dict[str, Dict[str, Segment]]) -> bool:
    for i in range(len(path) - 1):
        segment = all_segments[path[i]][path[i + 1]]
        if len(segment.dependencies.intersection(path[i + 1:])) != 0:
            return False
    return True


def length(path: Tuple, all_segments: Dict[str, Dict[str, Segment]]) -> int:
    path_length = 0
    for i in range(len(path) - 1):
        path_length += all_segments[path[i]][path[i + 1]].length
    return path_length


class Labyrinth:
    def __init__(self, map: str):
        self.map = np.array([
            [char for char in line]
            for line in map.split('\n')
        ]).transpose()

    def find_shortest_path(self) -> int:
        self.simplify()
        print('generate_all_segments started')
        all_segments = self.generate_all_segments()
        print('generate_all_segments done')
        all_keys = self.find_all_keys()
        print('checking valid segments started')
        paths = {
            ('@', *permutation)
            for permutation in permutations(all_keys)
            if is_valid(('@', *permutation), all_segments)
        }
        print('checking valid segments done')
        print('finding shortest started')
        shortest_path = min(paths, key=lambda path: length(path, all_segments))
        print('finding shortest done')
        print(shortest_path)
        return length(shortest_path, all_segments)

    def create_segment(self, start: str, end: str) -> Segment:
        segment = self.find_segment_bread_first(start, end)
        return Segment(
            length=len(segment) - 1,
            dependencies={
                self.map[step].lower()
                for step in segment
                if self.map[step] in ALPHABET.upper()
            }
        )

    def find_segment_bread_first(self, start: str, end: str) -> List[Tuple[int, int]]:
        start_location = self.locate(start)
        end_location = self.locate(end)
        segments = [[start_location]]
        while segments[0][-1] != end_location:
            segment = segments.pop(0)
            for option in self.find_options(segment[-1]):
                if option not in segment:
                    new_segment = [*segment, option]
                    segments.append(new_segment)
        return segments[0]

    def find_options(self, location: Tuple[int, int]) -> Set[Tuple[int, int]]:
        return {
            (location[0] + dx, location[1] + dy)
            for dx, dy in DIRECTIONS
            if self.map[location[0] + dx, location[1] + dy] != '#'
        }

    def find_all_keys(self) -> Set[str]:
        return {
            letter
            for letter in ALPHABET.lower()
            if self.locate(letter)
        }

    def locate(self, symbol: str) -> Tuple[int, int]:
        return tuple(
            x[0]
            for x in np.nonzero(self.map == symbol)
            if len(x) != 0
        )

    def generate_all_segments(self) -> Dict[str, Dict[str, Segment]]:
        return {
            start: {
                end: self.create_segment(start, end)
                for end in self.find_all_keys().difference({start})
            }
            for start in self.find_all_keys().union({'@'})
        }

    def simplify(self):
        simplified_in_last_iteration = True
        while simplified_in_last_iteration:
            simplified_in_last_iteration = False
            for i in range(self.map.shape[0]):
                for j in range(self.map.shape[1]):
                    # if . surrounded by 3 #
                    if (
                            self.map[i, j] in '.' + ALPHABET.upper()
                            and
                            len([
                                self.map[i + direction[0], j + direction[1]]
                                for direction in DIRECTIONS
                                if self.map[i + direction[0], j + direction[1]] == '#'
                            ]) == 3
                    ):
                        self.map[i, j] = '#'
                        simplified_in_last_iteration = True

    def __repr__(self) -> str:
        map = self.map.transpose()
        representation = ''
        for y in range(map.shape[0]):
            for x in range(map.shape[1]):
                representation += map[y, x]
            representation += '\n'
        return representation

    def measure(self, manual_path: str) -> int:
        length = 0
        for i in range(len(manual_path) - 1):
            segment = self.create_segment(manual_path[i], manual_path[i + 1])
            length += segment.length
        return length


class TestSilver(TestCase):
    EXAMPLE_0 = '''
        #########
        #b.A.@.a#
        #########
    '''.strip(' \n').replace(' ', '')

    def test_locate(self):
        labyrinth = Labyrinth(self.EXAMPLE_0)
        self.assertTupleEqual((5, 1), labyrinth.locate('@'))
        self.assertTupleEqual((7, 1), labyrinth.locate('a'))
        self.assertTupleEqual((3, 1), labyrinth.locate('A'))

    def test_find_segment_bread_first(self):
        labyrinth = Labyrinth(self.EXAMPLE_0)
        self.assertEqual(
            [(7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1)],
            labyrinth.find_segment_bread_first(start='a', end='b')
        )

    def test_create_segment(self):
        labyrinth = Labyrinth(self.EXAMPLE_0)
        self.assertEqual(
            Segment(length=6, dependencies={'a'}),
            labyrinth.create_segment(start='a', end='b')
        )

    def test_find_all_keys(self):
        labyrinth = Labyrinth(self.EXAMPLE_0)
        self.assertSetEqual(
            {'a', 'b'},
            labyrinth.find_all_keys()
        )

    def test_generate_all_segments(self):
        labyrinth = Labyrinth(self.EXAMPLE_0)
        self.assertDictEqual(
            {
                '@': {
                    'a': Segment(length=2, dependencies=set()),
                    'b': Segment(length=4, dependencies={'a'}),
                },
                'a': {
                    'b': Segment(length=6, dependencies={'a'})
                },
                'b': {
                    'a': Segment(length=6, dependencies={'a'})
                }
            },
            labyrinth.generate_all_segments()
        )

    def test_example_0(self):
        labyrinth = Labyrinth(self.EXAMPLE_0)
        self.assertEqual(
            8,
            labyrinth.find_shortest_path()
        )

    EXAMPLE_1 = '''
        ########################
        #f.D.E.e.C.b.A.@.a.B.c.#
        ######################.#
        #d.....................#
        ########################
    '''.strip(' \n').replace(' ', '')

    def test_example_1(self):
        labyrinth = Labyrinth(self.EXAMPLE_1)
        self.assertEqual(
            86,
            labyrinth.find_shortest_path()
        )

    def _test_assignement(self):
        with open('data.txt') as file:
            data = ''.join(file.readlines())
        labyrinth = Labyrinth(data)
        self.assertEqual(
            0,
            labyrinth.find_shortest_path()
        )

    def test_manual(self):
        with open('data.txt') as file:
            data = ''.join(file.readlines())
        labyrinth = Labyrinth(data)
        labyrinth.simplify()
        print(labyrinth)

        self.assertEqual(
            3832,
            labyrinth.measure('@bwcfsnqholrjupgmvkzxdytiae')
        )


class TestGold(TestCase):
    def test_manual(self):
        with open('data.txt') as file:
            data = ''.join(file.readlines())
        labyrinth = Labyrinth(data)
        center = labyrinth.locate('@')
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                labyrinth.map[center[0] + dx, center[0] + dy] = '#'
        labyrinth.map[center[0] - 1, center[0] - 1] = '@'
        labyrinth.map[center[0] + 1, center[0] - 1] = '$'
        labyrinth.map[center[0] + 1, center[0] + 1] = '%'
        labyrinth.map[center[0] - 1, center[0] + 1] = '&'
        labyrinth.simplify()
        print(labyrinth)

        manual_paths = [
            '@bwcfsnq',
            '&h',
            '$olr',
            '%jupg',
            'hm',
            'rv',
            'mkzxd',
            'vytiae'
        ]

        self.assertEqual(
            1724,
            sum([
                labyrinth.measure(manual_path)
                for manual_path in manual_paths
            ])
        )
