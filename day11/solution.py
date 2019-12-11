from unittest import TestCase
import seaborn as sns
import matplotlib.pyplot as plt

from shared.intcode import read_data, Intcode
from shared.ocr import ocr

BLACK = 0
WHITE = 1

UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
RIGHT = (1, 0)
TURN_LEFT = 0
TURN_LEFT_DICT = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}
TURN_RIGHT = 1
TURN_RIGHT_DICT = {UP: RIGHT, LEFT: UP, DOWN: LEFT, RIGHT: DOWN}


class Robot:
    def __init__(self, start_position, start_direction):
        self.position = start_position
        self.direction = start_direction

    def turn(self, turn):
        if turn == TURN_LEFT:
            self.direction = TURN_LEFT_DICT[self.direction]
        elif turn == TURN_RIGHT:
            self.direction = TURN_RIGHT_DICT[self.direction]
        else:
            raise Exception('turn command {} is not valid'.format(turn))

    def move(self):
        self.position = (
            self.position[0] + self.direction[0],
            self.position[1] + self.direction[1],
        )


class Hull:
    def __init__(self, original_painting={}):
        self.painted = original_painting

    def paint(self, position, color):
        self.painted[position] = color

    def get_color(self, position):
        if position in self.painted.keys():
            return self.painted[position]
        else:
            return BLACK


def solve(hull):
    intcode = Intcode(read_data(), inputs=[])
    robot = Robot((0, 0), UP)
    while not intcode.halted:
        intcode.run_program()
        if len(intcode.output) >= 2:
            color = intcode.output.pop(0)
            turn = intcode.output.pop(0)
            hull.paint(robot.position, color)
            robot.turn(turn)
            robot.move()

        intcode.add_input([hull.get_color(robot.position)])


class TestSilver(TestCase):
    def test_assignement(self):
        hull = Hull()

        solve(hull)

        self.assertEqual(
            len(hull.painted),
            1863
        )


class TestGold(TestCase):

    # BLULZJLZ
    def test_assignement(self):
        hull = Hull({(0, 0): WHITE})

        solve(hull)

        white_panels = [
            panel
            for panel in hull.painted.keys()
            if hull.painted[panel] == WHITE
        ]

        image = []
        for y in range(
                min([panel[1] for panel in white_panels]),
                max([panel[1] for panel in white_panels]) + 1
        ):
            row = []
            for x in range(
                    min([panel[0] for panel in white_panels]),
                    max([panel[0] for panel in white_panels]) + 1
            ):
                row.append(-hull.get_color((x, y)))
            image.append(row)

        for line in image:
            for cell in line:
                if cell == 0:
                    print('#', end='')
                else:
                    print('.', end='')
            print()

        self.assertEqual(
            ocr(image, blur=4),
            'BLULZJLZ'
        )
