from unittest import TestCase

import numpy as np

from shared.intcode import read_data, Intcode


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TestSilver(TestCase):
    def test_assignement(self):
        data = read_data()
        map = np.ones((50, 50), dtype=int) * -1
        for i in range(50):
            for j in range(50):
                intcode = Intcode(data.copy(), [])
                intcode.add_input([i, j])
                intcode.run_program()
                map[i, j] = intcode.output[0]

        self.assertEqual(
            183,
            np.count_nonzero(map == 1)
        )


def determine_left_wing(closest_point, size=100):
    return closest_point[0], closest_point[1] + size - 1


def determine_right_wing(closest_point, size=100):
    return closest_point[0] + size - 1, closest_point[1]


def is_outside_beam(point, code):
    intcode = Intcode(code.copy(), [])
    intcode.add_input([point[0], point[1]])
    intcode.run_program()
    return intcode.output[-1] == 0


def lef_wing_is_outside_beam(closest_point, data):
    left_wing = determine_left_wing(closest_point)
    return is_outside_beam(point=left_wing, code=data)


def right_wing_is_outside_beam(closest_point, data):
    right_wing = determine_right_wing(closest_point)
    return is_outside_beam(point=right_wing, code=data)


# 19161086 is to high
class TestGold(TestCase):
    def test_assignement(self):
        data = read_data()
        closest_point = (1, 1)
        while (
                lef_wing_is_outside_beam(closest_point, data)
                or
                right_wing_is_outside_beam(closest_point, data)
        ):
            while lef_wing_is_outside_beam(closest_point, data):
                closest_point = (closest_point[0] + 1, closest_point[1])
            while right_wing_is_outside_beam(closest_point, data):
                closest_point = (closest_point[0], closest_point[1] + 1)
        self.assertEqual(
            closest_point[0] * 10_000 + closest_point[1],
            11221248
        )

    def test_assignement_print_area(self):
        start = 50

        data = read_data()
        map = np.ones((50, 50), dtype=int) * -1
        for i in range(30):
            for j in range(30):
                intcode = Intcode(data.copy(), [])
                intcode.add_input([start + i, start + j])
                intcode.run_program()
                map[i, j] = intcode.output[0]

        for i in range(1, 30):
            for j in range(1, 30):
                print(
                    [' {:4}', '\033[93m {:4}\033[0m', ' {:4}'][map[i, j]].format(int((start + i) / (start + j) * 1000)),
                    end='')
            print()

        # beam upper limit has a direction: 0.832 - 0.833
        # beam lower limit has a direction: 0.976 - 0.984

    # rules for triangles: https://www.calculator.net/triangle-calculator.html
    def test_math(self):
        upper_rico = 0.832
        lower_rico = 0.984

        # angle of upper beam
        alpha = np.arctan(upper_rico)
        print('alpha: ', alpha)

        # angle of lower beam
        beta = np.arctan(lower_rico)
        print('beta: ', beta)

        # prolongation of upper side of the square till lower beam
        B = 100 / lower_rico
        print('B: ', B)

        # upper beam length till square corner
        A = (B + 100) / np.sin(beta - alpha) * np.sin(np.pi - beta)
        print('A: ', A)

        # y-coordinate of upper right corner of the square
        y = A / np.sin(np.pi / 2) * np.sin(alpha)
        print('y: ', y)

        # x-coordinate of upper right corner of the square
        x = np.sqrt(y ** 2 + A ** 2)
        print('x: ', x)

        x_closest = x - 100
        print('x-closest: ', x_closest)

        print('answer: ', np.ceil(x_closest) * 10_000 + np.ceil(y))

        print('rico: ', y / x)

    def test_positions(self):
        x = 900
        y = 1000
        data = read_data()
        intcode = Intcode(data.copy(), [])
        intcode.add_input([x, y])
        intcode.run_program()
        print('(x={}, y={}): {}'.format(x, y, intcode.output[0]))
