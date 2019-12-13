from functools import reduce
from typing import List
from unittest import TestCase

import numpy as np


def compare(value, reference):
    if value < reference:
        return -1
    elif value == reference:
        return 0
    elif value > reference:
        return 1
    else:
        raise Exception()


class Coord:
    def __init__(self, x: int, y: int, z: int):
        self.z = z
        self.y = y
        self.x = x

    def __repr__(self) -> str:
        return 'Coord(x={}, y={}, z={})'.format(self.x, self.y, self.z)

    def __eq__(self, other: 'Coord') -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def direction(self) -> 'Coord':
        return Coord(x=compare(self.x, 0), y=compare(self.y, 0), z=compare(self.z, 0))

    def energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def flatten(self):
        return [self.x, self.y, self.z]


class Moon:
    def __init__(self, pos: Coord, vel: Coord):
        self.vel = vel
        self.pos = pos

    def __repr__(self) -> str:
        return 'Moon(pos={}, vel={})'.format(self.pos, self.vel)

    def __eq__(self, other: 'Moon') -> bool:
        return self.pos == other.pos and self.vel == other.vel

    def accelerate(self, moons: List['Moon']) -> 'Moon':
        other_moons = moons.copy()
        other_moons.remove(self)
        return Moon(
            pos=self.pos,
            vel=self.vel + reduce(
                lambda a, b: a + b,
                [
                    (other_moon.pos - self.pos).direction()
                    for other_moon in other_moons
                ]
            )
        )

    def move(self) -> 'Moon':
        return Moon(pos=self.pos + self.vel, vel=self.vel)

    def energy(self) -> int:
        return self.pos.energy() * self.vel.energy()

    def flatten(self):
        return [*self.pos.flatten(), *self.vel.flatten()]


def generate(data):
    return [
        eval('Moon({})'.format(moon).replace('<', 'Coord(').replace('>', ')'))
        for moon in data.replace(' ', '').strip('\n').split('\n')
    ]


def accelerate(moons: List[Moon]) -> List[Moon]:
    return [
        moon.accelerate(moons)
        for moon in moons
    ]


def move(moons: List[Moon]) -> List[Moon]:
    return [
        moon.move()
        for moon in moons
    ]


def step(moons: List[Moon], times=1) -> List[Moon]:
    for _ in range(times):
        moons = move(accelerate(moons))
    return moons


def energy(moons: List[Moon]) -> int:
    return sum([
        moon.energy()
        for moon in moons
    ])


class TestSilver(TestCase):
    def test_example_a_same_moons_are_equal(self):
        moons = generate('''
            pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
            pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
            pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
            pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>
        ''')
        self.assertEqual(
            moons,
            generate('''
                pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
                pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
                pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
                pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>
            ''')
        )

    def test_example_0(self):
        moons = generate('''
            pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
            pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
            pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
            pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>
        ''')
        moons = step(moons)
        self.assertEqual(
            moons,
            generate('''
                pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
                pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
                pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
                pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>
            ''')
        )
        moons = step(moons, 9)
        self.assertEqual(
            moons,
            generate('''
                pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
                pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
                pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
                pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>
            ''')
        )
        self.assertEqual(
            energy(moons),
            179
        )

    def test_assignement(self):
        moons = generate('''
            pos=<x=3, y=3, z=0>, vel=<x=0, y=0, z=0>
            pos=<x=4, y=-16, z=2>, vel=<x=0, y=0, z=0>
            pos=<x=-10, y=-6, z=5>, vel=<x=0, y=0, z=0>
            pos=<x=-3, y=0, z=-13>, vel=<x=0, y=0, z=0>
        ''')
        moons = step(moons, 1000)
        self.assertEqual(
            energy(moons),
            12351
        )


def accelerate_gold(state):
    return tuple(
        (
            pos,
            vel + sum(
                [
                    compare(pos_other, pos)
                    for pos_other, _ in state
                ]
            )
        )
        for pos, vel in state
    )


def move_gold(state):
    return tuple(
        (pos + vel, vel)
        for pos, vel in state
    )


def step_gold(state):
    return move_gold(accelerate_gold(state))


def determine_period(start_positions):
    state = step_gold(start_positions)
    period = 1
    while state != start_positions:
        state = step_gold(state)
        period += 1
    print('period={}'.format(period))
    return period


class TestGold(TestCase):
    def test_example_0(self):
        # pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
        # pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
        # pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
        # pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>

        x = ((-1, 0), (2, 0), (4, 0), (3, 0))
        y = ((0, 0), (-10, 0), (-8, 0), (5, 0))
        z = ((2, 0), (-7, 0), (8, 0), (-1, 0))
        self.assertEqual(
            step_gold(x),
            ((2, 3), (3, 1), (1, -3), (2, -1))
        )
        self.assertEqual(
            np.lcm.reduce([determine_period(x), determine_period(y), determine_period(z)]),
            2772
        )

    def test_example(self):
        # <x=-8, y=-10, z=0>
        # <x=5, y=5, z=10>
        # <x=2, y=-7, z=3>
        # <x=9, y=-8, z=-3>

        x = ((-8, 0), (5, 0), (2, 0), (9, 0))
        y = ((-10, 0), (5, 0), (-7, 0), (-8, 0))
        z = ((0, 0), (10, 0), (3, 0), (-3, 0))

        self.assertEqual(
            np.lcm.reduce([determine_period(x), determine_period(y), determine_period(z)]),
            4686774924
        )

    def test_assignement(self):
        # pos=<x=3, y=3, z=0>, vel=<x=0, y=0, z=0>
        # pos=<x=4, y=-16, z=2>, vel=<x=0, y=0, z=0>
        # pos=<x=-10, y=-6, z=5>, vel=<x=0, y=0, z=0>
        # pos=<x=-3, y=0, z=-13>, vel=<x=0, y=0, z=0>

        x = ((3, 0), (4, 0), (-10, 0), (-3, 0))
        y = ((3, 0), (-16, 0), (-6, 0), (0, 0))
        z = ((0, 0), (2, 0), (5, 0), (-13, 0))

        period_z = determine_period(z)
        period_y = determine_period(y)
        period_x = determine_period(x)

        self.assertEqual(
            np.lcm.reduce([period_x, period_y, period_z]),
            380_635_029_877_596
        )
