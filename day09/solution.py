from unittest import TestCase

from shared.intcode import Intcode, read_data


class TestSilver(TestCase):
    def test_example_1(self):
        self.assertEqual(
            Intcode(
                [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99],
                []
            ).run_program(),
            [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        )

    def test_example_2(self):
        self.assertEqual(
            len(str(
                Intcode(
                    [1102, 34915192, 34915192, 7, 4, 7, 99, 0],
                    []
                ).run_program()[0]
            )),
            16
        )

    def test_example_3(self):
        self.assertEqual(
            Intcode(
                [104, 1125899906842624, 99],
                []
            ).run_program(),
            [1125899906842624]
        )

    def test_203(self):
        self.assertEqual(
            Intcode(
                [109, -2, 203, 2, 4, 0, 99],
                [1]
            ).run_program(),
            [1]
        )

    # 203 is to low
    def test_assignement(self):
        self.assertEqual(
            Intcode(
                read_data(),
                [1]
            ).run_program(),
            []
        )
