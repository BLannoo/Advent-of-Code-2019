from unittest import TestCase

from shared.intcode import Intcode, read_input


class TestSilver(TestCase):
    def test_example_0(self):
        self.assertEqual(
            Intcode([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]).run_program(),
            3500
        )

    def test_assignment(self):
        data = read_input()
        data[1] = 12
        data[2] = 2
        self.assertEqual(
            Intcode(data).run_program(),
            3085697
        )


class TestGold(TestCase):
    def test_assignement(self):
        for noun in range(100):
            for verb in range(100):
                data = read_input()
                data[1] = noun
                data[2] = verb
                if Intcode(data).run_program() == 19690720:
                    self.assertEqual(
                        100 * noun + verb,
                        9425
                    )
