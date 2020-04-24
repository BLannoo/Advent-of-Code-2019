import re
from typing import Set
from unittest import TestCase

from shared.intcode import Intcode, read_data


def execute_1_command(command, intcode):
    intcode.input_ascii(command + '\n')
    intcode.run_program()
    response = intcode.output_ascii()
    intcode.output = []
    return response


def gather_all_items(intcode):
    commands = [
        'north', 'take wreath', 'east', 'east', 'east', 'take weather machine',
        'west', 'west', 'west', 'south',
        'south', 'south', 'take candy cane',
        'north', 'west', 'take prime number', 'west', 'take astrolabe',
        'east', 'east', 'north', 'east', 'take food ration',
        'south', 'east', 'south', 'take hypercube',
        'east', 'take space law space brochure',
        'north', 'inv',
    ]
    for command in commands:
        execute_1_command(command, intcode)


ITEMS = {
    'candy cane', 'wreath', 'hypercube', 'food ration',
    'weather machine', 'space law space brochure', 'prime number', 'astrolabe',
}


class Bag:
    def __init__(self, content: Set[str], name: str = '?'):
        self.name = name
        self.content = content

    @staticmethod
    def bag_with_all_but(item: str):
        return Bag(
            content=ITEMS.difference({item}),
            name=f'bag without {item}'
        )

    @staticmethod
    def bag_with_required_items_and(item, REQUIRED_ITEMS):
        return Bag(
            content=REQUIRED_ITEMS.union({item}),
            name=f'bag with required and {item}'
        )

    def test_bag(self, intcode: Intcode) -> str:
        for item in ITEMS:
            if item in self.content:
                execute_1_command('take ' + item, intcode)
            else:
                execute_1_command('drop ' + item, intcode)

        execute_1_command('inv', intcode)
        response = execute_1_command('west', intcode)
        print(response)
        return re.search(
            r'Alert! Droids on this ship are (lighter|heavier) than the detected value!',
            response.replace('\n', ' ')
        )[1]

    def __repr__(self):
        return self.name


class TestSilver(TestCase):
    def test(self):
        data = read_data()
        intcode = Intcode(instructions=data, inputs=[])

        gather_all_items(intcode)

        bags = {
            Bag.bag_with_all_but(item)
            for item in ITEMS
        }
        for bag in bags:
            print(bag.test_bag(intcode), end=': ')
            print(bag)

        REQUIRED_ITEMS = {'food ration', 'candy cane'}

        bags = {
            Bag.bag_with_required_items_and(item, REQUIRED_ITEMS)
            for item in ITEMS.difference(REQUIRED_ITEMS)
        }
        for bag in bags:
            print(bag.test_bag(intcode), end=': ')
            print(bag)

        # TOO_HEAVY = {'hypercube', 'weather machine', 'wreath'}
        # EXTRA_ITEMS = {'astrolabe', 'space law space brochure', 'prime number'}

        FINAL_OPTIONS = [
            {'astrolabe', 'space law space brochure', 'prime number'},
            {'astrolabe', 'space law space brochure'},
            {'astrolabe', 'prime number'},
            {'space law space brochure', 'prime number'},
        ]
        bags = {
            Bag(REQUIRED_ITEMS.union(option))
            for option in FINAL_OPTIONS
        }
        for bag in bags:
            print(bag.test_bag(intcode), end=': ')
            print(bag)

        # while True:
        #     execute_1_command(input(), intcode)
