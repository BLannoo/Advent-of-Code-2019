import re
from typing import List, Callable
from unittest import TestCase


def deal_into_new_stack(cards: List[int]) -> None:
    cards.reverse()


def cut(n: int, cards: List[int]) -> List[int]:
    return cards[n:] + cards[:n]


def deal_with_increment(n: int, cards: List[int]) -> List[int]:
    num_cards = len(cards)
    stack = [-1] * num_cards
    for i, card in enumerate(cards):
        stack[(i * n) % num_cards] = card
    return stack


class TestSilver(TestCase):
    def test_deal_into_new_stack(self):
        cards = list(range(10))
        deal_into_new_stack(cards)
        self.assertListEqual(
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            cards
        )

    def test_cut(self):
        cards = list(range(10))
        cards = cut(3, cards)
        self.assertListEqual(
            [3, 4, 5, 6, 7, 8, 9, 0, 1, 2],
            cards
        )

    def test_cut_negative(self):
        cards = list(range(10))
        cards = cut(-4, cards)
        self.assertListEqual(
            [6, 7, 8, 9, 0, 1, 2, 3, 4, 5],
            cards
        )

    def test_deal_with_increment(self):
        cards = list(range(10))
        cards = deal_with_increment(3, cards)
        self.assertListEqual(
            [0, 7, 4, 1, 8, 5, 2, 9, 6, 3],
            cards
        )

    def test_example_0(self):
        self.assertListEqual(
            [0, 3, 6, 9, 2, 5, 8, 1, 4, 7],
            solve_silver(
                deck_size=10,
                instructions='''
                    deal with increment 7
                    deal into new stack
                    deal into new stack
                '''.strip(' \n').replace('  ', '')
            )
        )

    def test_example_1(self):
        self.assertListEqual(
            [3, 0, 7, 4, 1, 8, 5, 2, 9, 6],
            solve_silver(
                deck_size=10,
                instructions='''
                    cut 6
                    deal with increment 7
                    deal into new stack
                '''.strip(' \n').replace('  ', '')
            )
        )

    def test_example_2(self):
        self.assertListEqual(
            [6, 3, 0, 7, 4, 1, 8, 5, 2, 9],
            solve_silver(
                deck_size=10,
                instructions='''
                    deal with increment 7
                    deal with increment 9
                    cut -2
                '''.strip(' \n').replace('  ', '')
            )
        )

    def test_example_3(self):
        self.assertListEqual(
            [9, 2, 5, 8, 1, 4, 7, 0, 3, 6],
            solve_silver(
                deck_size=10,
                instructions='''
                    deal into new stack
                    cut -2
                    deal with increment 7
                    cut 8
                    cut -4
                    deal with increment 7
                    cut 3
                    deal with increment 9
                    deal with increment 3
                    cut -1
                '''.strip(' \n').replace('  ', '')
            )
        )

    def test_assignement(self):
        with open('data.txt') as file:
            instructions = '\n'.join(file.readlines())
        self.assertEqual(
            4649,
            solve_silver(deck_size=10_007, instructions=instructions).index(2019)
        )


def solve_silver(deck_size: int, instructions: str) -> List[int]:
    cards = list(range(deck_size))
    for instruction in instructions.split('\n'):

        match = re.search(pattern=r'deal with increment (\d+)', string=instruction)
        if match:
            cards = deal_with_increment(int(match.group(1)), cards)
            continue

        match = re.search(pattern=r'cut (-?\d+)', string=instruction)
        if match:
            cards = cut(int(match.group(1)), cards)

        match = re.search(pattern=r'deal into new stack', string=instruction)
        if match:
            deal_into_new_stack(cards)

    return cards


class ModuloCalculusStep:
    def __init__(self, factor: int, term: int, modulo: int):
        self.factor = factor
        self.term = term
        self.modulo = modulo

    def __call__(self, *args: int, **kwargs) -> int:
        return (args[0] * self.factor + self.term) % self.modulo

    def merge(self, other: 'ModuloCalculusStep') -> 'ModuloCalculusStep':
        if self.modulo != other.modulo:
            raise Exception(
                f'Can not merge ModuloCalculusStep with different modulos: {self.modulo} and {other.modulo}'
            )
        return ModuloCalculusStep(
            factor=(self.factor * other.factor) % self.modulo,
            term=(self.term * other.factor + other.term) % self.modulo,
            modulo=self.modulo
        )

    def inverse(self, card: int) -> float:

        # algorithm for the modular multiplicative inverse:
        # https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
        def egcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                g, y, x = egcd(b % a, a)
                return g, x - (b // a) * y, y

        def modinv(a, m):
            g, x, y = egcd(a, m)
            if g != 1:
                raise Exception('modular inverse does not exist')
            else:
                return x % m

        inverse_factor = modinv(self.factor, self.modulo)
        return (card * inverse_factor - self.term * inverse_factor) % self.modulo

    def __repr__(self):
        return f'(a * {self.factor} + {self.term}) % {self.modulo}'


def parse_instruction(deck_size: int, instruction: str) -> ModuloCalculusStep:
    match_deal_with_increment = re.search(pattern=r'deal with increment (\d+)', string=instruction)
    match_cut = re.search(pattern=r'cut (-?\d+)', string=instruction)
    if match_deal_with_increment:
        n = int(match_deal_with_increment.group(1))
        command = ModuloCalculusStep(n, 0, deck_size)
    elif match_cut:
        n = int(match_cut.group(1))
        command = ModuloCalculusStep(1, -n, deck_size)
    else:
        command = ModuloCalculusStep(-1, deck_size - 1, deck_size)
    return command


def parse_instructions(deck_size, instructions):
    return [
        parse_instruction(deck_size, instruction)
        for instruction in instructions.split('\n')
    ]


def simplify(commands: List[ModuloCalculusStep]) -> ModuloCalculusStep:
    command = commands[0]
    for i in range(1, len(commands)):
        command = command.merge(commands[i])
    return command


def solve_gold(deck_size: int, instructions: str, iterations: int) -> ModuloCalculusStep:
    commands = parse_instructions(deck_size, instructions)

    command_single_iteration = simplify(commands)

    binary = [d == '1' for d in bin(iterations)[2:]]

    shuffle_power_2_iterations = [command_single_iteration] * len(binary)
    shuffle_power_2_iterations[0] = command_single_iteration
    for i in range(1, len(binary)):
        shuffle_power_2_iterations[i] = shuffle_power_2_iterations[i - 1].merge(shuffle_power_2_iterations[i - 1])

    command_full = ModuloCalculusStep(1, 0, deck_size)
    for i in range(len(binary)):
        if binary[i]:
            command_full = command_full.merge(shuffle_power_2_iterations[-i - 1])

    return command_full


class TestGold(TestCase):
    def test_example_0(self):
        self.assertEqual(
            9,
            solve_gold(
                deck_size=10,
                instructions='''
                                deal with increment 7
                                deal into new stack
                                deal into new stack
                            '''.strip(' \n').replace('  ', ''),
                iterations=1
            )(7)
        )

    def test_example_1(self):
        self.assertEqual(
            2,
            solve_gold(
                deck_size=10,
                instructions='''
                            cut 6
                            deal with increment 7
                            deal into new stack
                        '''.strip(' \n').replace('  ', ''),
                iterations=1
            )(7)
        )

    def test_example_2(self):
        self.assertEqual(
            3,
            solve_gold(
                deck_size=10,
                instructions='''
                                deal with increment 7
                                deal with increment 9
                                cut -2
                            '''.strip(' \n').replace('  ', ''),
                iterations=1
            )(7)
        )

    def test_example_3(self):
        self.assertEqual(
            6,
            solve_gold(
                deck_size=10,
                instructions='''
                                deal into new stack
                                cut -2
                                deal with increment 7
                                cut 8
                                cut -4
                                deal with increment 7
                                cut 3
                                deal with increment 9
                                deal with increment 3
                                cut -1
                            '''.strip(' \n').replace('  ', ''),
                iterations=1
            )(7)
        )

    def test_silver(self):
        with open('data.txt') as file:
            instructions = ''.join(file.readlines())
        self.assertEqual(
            4649,
            solve_gold(
                deck_size=10_007,
                instructions=instructions,
                iterations=1
            )(2019)
        )

    def test_silver_iterate_twice_same_as_2_iterations(self):
        with open('data.txt') as file:
            instructions = ''.join(file.readlines())

        def partial(card: int, iterations: int) -> int:
            return solve_gold(
                deck_size=10_007,
                instructions=instructions,
                iterations=iterations
            )(card)

        self.assertEqual(
            partial(partial(2019, 1), 1),
            partial(2019, 2)
        )

    def test_silver_other_iterations(self):
        with open('data.txt') as file:
            instructions = ''.join(file.readlines())

        def partial(card: int, iterations: int) -> int:
            return solve_gold(
                deck_size=10_007,
                instructions=instructions,
                iterations=iterations
            )(card)

        def iterate_partial(card, times):
            for _ in range(times):
                card = partial(card, 1)
            return card

        iterations = 562
        self.assertEqual(
            iterate_partial(2019, iterations),
            partial(2019, iterations)
        )

    # 60363464405545 is too low (question is inverse)
    def test_assignement(self):
        with open('data.txt') as file:
            instructions = ''.join(file.readlines())
        self.assertEqual(
            68849657493596,
            solve_gold(
                deck_size=119_315_717_514_047,
                instructions=instructions,
                iterations=101_741_582_076_661
            ).inverse(2020)
        )
