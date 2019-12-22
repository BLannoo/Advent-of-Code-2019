from abc import ABC, abstractmethod
from typing import List, Dict
from unittest import TestCase

from shared.intcode import Intcode, read_data


class Rule(ABC):

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def execute(self, variables: Dict[str, bool]) -> Dict[str, bool]:
        pass


class InnertRule(Rule):
    def __init__(self, command: str):
        self.command = command

    def execute(self, variables: Dict[str, bool]) -> Dict[str, bool]:
        return variables

    def __repr__(self) -> str:
        return self.command


class Not(Rule):
    def __init__(self, x: str, y: str):
        self.x = x
        self.y = y

    def execute(self, variables: Dict[str, bool]) -> Dict[str, bool]:
        exec(f'variables["{self.y}"] = not variables["{self.x}"]')
        return variables

    def __repr__(self) -> str:
        return f'NOT {self.x} {self.y}'


class Or(Rule):
    def __init__(self, x: str, y: str):
        self.x = x
        self.y = y

    def execute(self, variables: Dict[str, bool]) -> Dict[str, bool]:
        exec(f'variables["{self.y}"] = variables["{self.y}"] or variables["{self.x}"]')
        return variables

    def __repr__(self):
        return f'OR {self.x} {self.y}'


class And(Rule):
    def __init__(self, x: str, y: str):
        self.x = x
        self.y = y

    def execute(self, variables: Dict[str, bool]) -> Dict[str, bool]:
        exec(f'variables["{self.y}"] = variables["{self.y}"] and variables["{self.x}"]')
        return variables

    def __repr__(self):
        return f'AND {self.x} {self.y}'


def print_illustration(ground, jumps):
    behaviour = ['-' for _ in range(len(ground))]
    for jump in jumps:
        if behaviour[jump - 1] == '-':
            behaviour[jump - 1] = '^'
        else:
            behaviour[jump - 1] = 'X'
        behaviour[jump - 1 + 4] = 'v'
    print(''.join(behaviour))
    print(ground)
    if len(jumps) > 0:
        print('-' * jumps[0] + 'ABCDEFGHI')
    print(''.join(map(str, range(10))))


class Rules:
    def __init__(self):
        self.rules: List[Rule] = []

    def add(self, rule: Rule) -> None:
        self.rules.append(rule)

    def __repr__(self) -> str:
        return '\n'.join([str(rule) for rule in self.rules]) + '\n'

    def jump(self, variables: Dict[str, bool]) -> bool:
        for rule in self.rules:
            variables = rule.execute(variables)
        return variables['J']

    def test(self, ground: str) -> List[int]:
        ground += '########'
        jumps = []
        i = 0
        while i < len(ground) - 8:
            variables = {
                'A': ground[i] == '#',
                'B': ground[i + 1] == '#',
                'C': ground[i + 2] == '#',
                'D': ground[i + 3] == '#',
                'E': ground[i + 4] == '#',
                'F': ground[i + 5] == '#',
                'G': ground[i + 6] == '#',
                'H': ground[i + 7] == '#',
                'I': ground[i + 8] == '#',
                'T': False,
                'J': False
            }
            if self.jump(variables):
                jumps.append(i)
                i += 2  # skip 2 more when jumping
            i += 1
        print_illustration(ground, jumps)
        return jumps


walking = Rules()
walking.add(Not('A', 'J'))
walking.add(Not('B', 'T'))
walking.add(Or('T', 'J'))
walking.add(Not('C', 'T'))
walking.add(Or('T', 'J'))
walking.add(And('D', 'J'))
walking.add(InnertRule('WALK'))


class TestSilver(TestCase):
    def test_1(self):
        self.assertIn(
            member=walking.test(ground='#####.###########'),
            container=([3], [4], [5])
        )

    def test_2(self):
        self.assertIn(
            member=walking.test(ground='#####.##.########'),
            container=([3, 6], [4, 7])
        )

    def test_3(self):
        self.assertIn(
            member=walking.test(ground='#####...#########'),
            container=([5],)
        )

    def test_assignement(self):
        intcode = Intcode(read_data(), [])
        print('--- start printing rules ---\n' + str(walking) + '\n--- finished printing rules ---')
        intcode.input_ascii(
            str(walking)
        )
        intcode.run_program()
        print(intcode.output_ascii())
        self.assertEqual(
            19357534,
            intcode.output[-1]
        )


running = Rules()

running.add(Not('A', 'J'))
running.add(Not('B', 'T'))
running.add(Or('T', 'J'))
running.add(Not('C', 'T'))
running.add(Or('T', 'J'))
running.add(And('D', 'J'))

running.add(Not('I', 'T'))
running.add(Not('T', 'T'))
running.add(Or('F', 'T'))
running.add(And('E', 'T'))
running.add(Or('H', 'T'))
running.add(And('T', 'J'))

running.add(InnertRule('RUN'))


class TestGold(TestCase):
    def test_1(self):
        self.assertIn(
            member=running.test(ground='#####.#.#...#####'),
            container=([5, 9],)
        )

    def test_2(self):
        self.assertIn(
            member=running.test(ground='#####..###...####'),
            container=([4, 10], [5, 10])
        )

    def test_3(self):
        self.assertIn(
            member=running.test(ground='#####..####...###'),
            container=([4, 11], [5, 11])
        )

    def test_assignement(self):
        intcode = Intcode(read_data(), [])
        print('--- start printing rules ---\n' + str(running) + '\n--- finished printing rules ---')
        intcode.input_ascii(
            str(running)
        )
        intcode.run_program()
        print(intcode.output_ascii())
        self.assertEqual(
            1142814363,
            intcode.output[-1]
        )
