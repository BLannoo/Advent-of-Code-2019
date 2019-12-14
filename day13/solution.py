from typing import Tuple
from unittest import TestCase

import pygame

from day12.solution import compare
from shared.intcode import read_data, Intcode


class TestSilver(TestCase):
    def test_assignement(self):
        data = Intcode(read_data(), inputs=[]).run_program()
        self.assertEqual(
            sum(1 for type in data[2::3] if type == 2),
            268
        )


class Arcade:
    def __init__(self, program):
        self.intcode = Intcode(program, inputs=[0, 0, 0])
        data = self.intcode.run_program()
        self.state = self.parse_output(data)
        self.max_x, self.max_y = max(self.state.keys())
        self.intcode.output = []

    @staticmethod
    def parse_output(data):
        return {
            (data[i * 3], data[i * 3 + 1]): data[i * 3 + 2]
            for i in range(int(len(data) / 3))
        }

    @staticmethod
    def create() -> 'Arcade':
        program = read_data()
        program[0] = 2
        return Arcade(program)

    def score(self):
        return self.state[(-1, 0)]

    def __repr__(self):
        representation = 'Your score is: {}\n'.format(self.state[(-1, 0)])
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                tile_id = self.state[(x, y)]
                if tile_id == 0:
                    representation += '.'
                elif tile_id == 1:
                    representation += '#'
                elif tile_id == 2:
                    representation += 'x'
                elif tile_id == 3:
                    representation += '-'
                elif tile_id == 4:
                    representation += 'O'
                else:
                    representation += int(tile_id)
            representation += '\n'
        return representation

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((10 * (self.max_x + 1), 10 * (self.max_y + 1)))
        done = False

        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.move_joystick(-1)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.move_joystick(1)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.move_joystick(0)

            screen.fill((0, 0, 0))
            self.draw_state(screen)

            pygame.display.flip()
            clock.tick(1)

    def move_joystick(self, move):
        self.intcode.add_input([move])
        for coords, tile_id in Arcade.parse_output(self.intcode.run_program()).items():
            self.state[coords] = tile_id
        self.intcode.output = []

    def draw_state(self, screen) -> None:
        colors = {
            0: (0, 0, 0),
            1: (255, 255, 255),
            2: (100, 100, 100),
            3: (255, 0, 0),
            4: (0, 255, 0)
        }
        for (x, y), tile_id in self.state.items():
            if x == -1:
                print("Your score is: {}".format(tile_id))
                continue
            pygame.draw.rect(
                screen,
                colors[tile_id],
                pygame.Rect(x * 10, y * 10, 10, 10)
            )

    def find(self, target: int) -> Tuple[int, int]:
        return tuple(
            (x, y)
            for (x, y), tile_id in self.state.items()
            if tile_id == target
        )[0]


class TestGold(TestCase):
    def test_assignement(self):
        arcade = Arcade.create()
        while not arcade.intcode.halted:
            arcade.move_joystick(
                compare(arcade.find(4)[0], arcade.find(3)[0])
            )

        self.assertEqual(
            arcade.state[(-1, 0)],
            13989
        )

    def test_manual(self):
        arcade = Arcade.create()
        arcade.run()
