from math import ceil
from typing import Tuple
from unittest import TestCase


class Reaction:
    def __init__(self, output_chemical: Tuple[str, int], input_chemicals: Tuple):
        self.input_chemicals = input_chemicals
        self.output_chemical = output_chemical

    @staticmethod
    def create(description: str) -> 'Reaction':
        input_chemicals, output_chemical = description.split('=>')
        return Reaction(
            Reaction.parse_single_term(output_chemical),
            tuple(
                Reaction.parse_single_term(input_chemical)
                for input_chemical in input_chemicals.split(',')
            )
        )

    @staticmethod
    def parse_single_term(single_term: str) -> Tuple[str, int]:
        parts = single_term.strip('\n ').split(' ')
        return parts[1], int(parts[0])

    def __repr__(self):
        return 'Reaction(output_chemical={}, input_chemicals={})'.format(
            self.output_chemical,
            self.input_chemicals
        )


def read_rules(filename='data.txt'):
    with open(filename) as file:
        reactions = {
            reaction.output_chemical[0]: reaction
            for reaction in [
                Reaction.create(line)
                for line in file
            ]
        }
    return reactions


def needed_chemicals(needed):
    return [
        chemical
        for chemical, needed_quantity in needed.items()
        if needed_quantity != 0 and chemical != 'ORE'
    ]


def solve_silver(reactions):
    needed = {component: 0 for component in reactions.keys()}
    needed['FUEL'] = 1
    needed['ORE'] = 0
    extra = {component: 0 for component in reactions.keys()}
    while len(needed_chemicals(needed)) != 0:
        chemical = needed_chemicals(needed)[0]
        needed_quantity = needed[chemical]
        needed[chemical] = 0
        if needed_quantity <= extra[chemical]:
            extra[chemical] -= needed_quantity
            continue
        reaction = reactions[chemical]
        generated_quantity = reaction.output_chemical[1]
        reaction_quantity = ceil((needed_quantity - extra[chemical]) / generated_quantity)
        extra[chemical] += reaction_quantity * generated_quantity - needed_quantity
        for input_chemical in reaction.input_chemicals:
            needed[input_chemical[0]] += input_chemical[1]*reaction_quantity

    print(extra)
    print(needed)

    return needed


class TestSilver(TestCase):
    def test_example0(self):
        reactions = read_rules('example0.txt')
        needed = solve_silver(reactions)
        self.assertEqual(
            needed['ORE'],
            31
        )

    def test_example1(self):
        reactions = read_rules('example1.txt')
        needed = solve_silver(reactions)
        self.assertEqual(
            needed['ORE'],
            165
        )

    # 1786 too low
    def test_assignement(self):
        reactions = read_rules('data.txt')
        needed = solve_silver(reactions)
        self.assertEqual(
            needed['ORE'],
            1037742
        )
