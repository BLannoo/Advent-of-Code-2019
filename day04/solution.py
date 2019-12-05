from unittest import TestCase


def silver_constraints(i):
    digits = str(i)
    for j in range(len(digits) - 1):
        if digits[j] > digits[j + 1]:
            return False
    for j in range(len(digits) - 1):
        if digits[j] == digits[j + 1]:
            return True
    return False


def gold_constraints(i):
    digits = str(i)
    for j in range(len(digits) - 1):
        if digits[j] > digits[j + 1]:
            return False
    for j in range(len(digits) - 1):
        if (
                (digits[j] == digits[j + 1])
                and
                (j == 0 or digits[j - 1] != digits[j])
                and
                (j == 4 or digits[j + 2] != digits[j])
        ):
            return True
    return False


def solve(lower_bound, upper_bound, constraint):
    options = [
        i
        for i in range(lower_bound, upper_bound)
        if constraint(i)
    ]
    return len(options)


class TestGold(TestCase):
    def test_assignement(self):
        self.assertEqual(
            solve(367479, 893698, gold_constraints),
            305
        )

    def test_example_1(self):
        self.assertEqual(
            gold_constraints(112233),
            True
        )

    def test_example_2(self):
        self.assertEqual(
            gold_constraints(123444),
            False
        )

    def test_example_3(self):
        self.assertEqual(
            gold_constraints(111122),
            True
        )


class TestSilver(TestCase):
    def test_assignement(self):
        self.assertEqual(
            solve(367479, 893698, silver_constraints),
            495
        )

    def test_example_0(self):
        self.assertEqual(
            silver_constraints(122345),
            True
        )

    def test_example_1(self):
        self.assertEqual(
            silver_constraints(111111),
            True
        )

    def test_example_2(self):
        self.assertEqual(
            silver_constraints(223450),
            False
        )

    def test_example_3(self):
        self.assertEqual(
            silver_constraints(123789),
            False
        )
