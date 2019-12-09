from unittest import TestCase

from shared.intcode import Intcode, read_input


class TestSilver(TestCase):
    def test_example_a(self):
        self.assertEqual(
            Intcode([3, 0, 4, 0, 99], [3862]).run_program(),
            [3862]
        )

    def test_example_b(self):
        self.assertEqual(
            Intcode(
                [1002, 4, 3, 4, 33]
            ).run_program(),
            1002
        )

    def test_assignment(self):
        self.assertEqual(
            Intcode(read_input(), [1]).run_program(),
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 13285749]
        )


class TestGold(TestCase):
    def test_example_1(self):
        self.assertEqual(
            Intcode([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8]).run_program(),
            [1]
        )
        self.assertEqual(
            Intcode([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [7]).run_program(),
            [0]
        )

    def test_example_2(self):
        self.assertEqual(
            Intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [7]).run_program(),
            [1]
        )
        self.assertEqual(
            Intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8]).run_program(),
            [0]
        )
        self.assertEqual(
            Intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [9]).run_program(),
            [0]
        )

    def test_example_3(self):
        self.assertEqual(
            Intcode([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8]).run_program(),
            [1]
        )
        self.assertEqual(
            Intcode([3, 3, 1108, -1, 8, 3, 4, 3, 99], [7]).run_program(),
            [0]
        )

    def test_example_4(self):
        self.assertEqual(
            Intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99], [7]).run_program(),
            [1]
        )
        self.assertEqual(
            Intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8]).run_program(),
            [0]
        )
        self.assertEqual(
            Intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99], [9]).run_program(),
            [0]
        )

    def test_example_5(self):
        self.assertEqual(
            Intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0]).run_program(),
            [0]
        )
        self.assertEqual(
            Intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [9]).run_program(),
            [1]
        )

    def test_example_6(self):
        self.assertEqual(
            Intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0]).run_program(),
            [0]
        )
        self.assertEqual(
            Intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [9]).run_program(),
            [1]
        )

    def test_example_7(self):
        self.assertEqual(
            Intcode(
                [
                    3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                    1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                    999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
                ],
                [7]
            ).run_program(),
            [999]
        )
        self.assertEqual(
            Intcode(
                [
                    3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                    1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                    999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
                ],
                [8]
            ).run_program(),
            [1000]
        )
        self.assertEqual(
            Intcode(
                [
                    3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                    1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                    999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
                ],
                [9]
            ).run_program(),
            [1001]
        )

    def test_assignement(self):
        self.assertEqual(
            Intcode(read_input(), [5]).run_program(),
            [5000972]
        )
