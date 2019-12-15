from collections import defaultdict
from typing import List
from unittest import TestCase

from shared.intcode import read_data, Intcode

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

EMPTY = 1
WALL = 0
OXYGEN = 2

movements = {
    NORTH: lambda coords: (coords[0], coords[1] - 1),
    SOUTH: lambda coords: (coords[0], coords[1] + 1),
    WEST: lambda coords: (coords[0] - 1, coords[1]),
    EAST: lambda coords: (coords[0] + 1, coords[1]),
}

turn_right = {
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST,
    WEST: NORTH,
}

turn_left = {
    NORTH: WEST,
    WEST: SOUTH,
    SOUTH: EAST,
    EAST: NORTH,
}


def neighbours(coord):
    return [
        (coord[0] + delta[0], coord[1] + delta[1])
        for delta in ((1, 0), (0, 1), (-1, 0), (0, -1))
    ]


class RepairDroid:
    def __init__(self, program: List[int]):
        self.intcode = Intcode(program, [])
        self.intcode.run_program()
        self.map = defaultdict(lambda: '?')
        self.map[(0, 0)] = 'X'
        self.current_location = (0, 0)
        self.current_direction = NORTH
        self.fewest_movements = 0

    def solve_silver(self):
        response = EMPTY
        while response != OXYGEN:
            response = self.move()
        self.print_map()
        return self.fewest_movements

    def solve_gold(self):
        response = EMPTY
        while response != OXYGEN:
            response = self.move()
        oxygen_boundary = [self.current_location]
        while self.current_location != (0, 0):
            self.move()
        time = 0
        while '.' in self.map.values():
            oxygen_boundary = [
                outside_coord
                for inside_coord in oxygen_boundary
                for outside_coord in neighbours(inside_coord)
                if self.map[outside_coord] == '.'
            ]
            for outside_coord in oxygen_boundary:
                self.map[outside_coord] = 'O'
            time += 1
        return time

    def move(self):
        response = self.send_move_command(self.current_direction)
        destination = movements[self.current_direction](self.current_location)
        if response == EMPTY:
            if destination in self.map.keys():
                self.fewest_movements -= 1
            else:
                self.fewest_movements += 1
            self.current_location = destination
            self.current_direction = turn_right[self.current_direction]
            self.map[self.current_location] = '.'
        elif response == WALL:
            self.current_direction = turn_left[self.current_direction]
            self.map[destination] = '#'
        elif response == OXYGEN:
            self.fewest_movements += 1
            self.current_location = destination
            self.map[destination] = 'O'
        else:
            raise Exception('invalid response: {}'.format(response))
        return response

    def send_move_command(self, direction):
        self.intcode.add_input([direction])
        self.intcode.run_program()
        response = self.intcode.output[0]
        self.intcode.output = []
        return response

    def print_map(self):
        x_min = min(self.map.keys(), key=lambda coords: coords[0])[0]
        x_max = max(self.map.keys(), key=lambda coords: coords[0])[0]
        y_min = min(self.map.keys(), key=lambda coords: coords[1])[1]
        y_max = max(self.map.keys(), key=lambda coords: coords[1])[1]

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                print(self.map[(x, y)], end='')
            print()


class TestSilver(TestCase):
    # 215 is too low: forgot the command to reach the oxygen
    def test_assignement(self):
        droid = RepairDroid(program=read_data())
        self.assertEqual(
            droid.solve_silver(),
            216
        )


class TestGold(TestCase):
    def test_assignement(self):
        droid = RepairDroid(program=read_data())
        self.assertEqual(
            droid.solve_gold(),
            326
        )
