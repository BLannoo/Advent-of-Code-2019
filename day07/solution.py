from itertools import permutations
from unittest import TestCase

from shared.intcode import Intcode, read_data


def amplification_sequence(phase_sequence, program):
    amplifiers = [
        Intcode(program, [phase])
        for phase in phase_sequence
    ]
    output = [0]
    current_amplifier = 0
    while not amplifiers[current_amplifier].halted:
        amplifiers[current_amplifier].add_input(output)
        output = amplifiers[current_amplifier].run_program()
        print('amplifier ', current_amplifier, ' output ', output)
        amplifiers[current_amplifier].output = []
        current_amplifier = (current_amplifier + 1) % len(phase_sequence)

    return output[0]


class TestSilver(TestCase):
    def test_example_1(self):
        program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
        phase_sequence = [4, 3, 2, 1, 0]

        self.assertEqual(
            amplification_sequence(phase_sequence, program),
            43210
        )

    def test_example_2(self):
        program = [
            3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
            101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0
        ]
        phase_sequence = [0, 1, 2, 3, 4]

        self.assertEqual(
            amplification_sequence(phase_sequence, program),
            54321
        )

    def test_example_3(self):
        program = [
            3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
            1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0
        ]
        phase_sequence = [1, 0, 4, 3, 2]

        self.assertEqual(
            amplification_sequence(phase_sequence, program),
            65210
        )

    def test_assignment(self):
        program = read_data()

        self.assertEqual(
            max([
                amplification_sequence(phase_sequence, program)
                for phase_sequence in permutations(range(5))
            ]),
            272368
        )


class TestGold(TestCase):
    def test_example_1(self):
        program = [
            3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
            27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5
        ]
        phase_sequence = [9, 8, 7, 6, 5]

        self.assertEqual(
            amplification_sequence(phase_sequence, program),
            139629729
        )

    def test_example_2(self):
        program = [
            3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
            -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
            53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10
        ]
        phase_sequence = [9, 7, 8, 5, 6]

        self.assertEqual(
            amplification_sequence(phase_sequence, program),
            18216
        )

    # 2526030 to low due to range(5, 9)
    def test_assignment(self):
        program = read_data()

        self.assertEqual(
            max([
                amplification_sequence(phase_sequence, program)
                for phase_sequence in permutations(range(5, 10))
            ]),
            19741286
        )
