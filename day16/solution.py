from functools import lru_cache
from itertools import islice
from unittest import TestCase

import numpy as np
from nptyping import Array


def fft(input_signal: str) -> str:
    input_signal_vector = digits(input_signal)
    n = input_signal_vector.shape[0]
    output_signal_vector = matrix(n).dot(input_signal_vector)
    return number(output_signal_vector)


def number(output_signal_vector: Array[int]) -> str:
    n = output_signal_vector.shape[0]
    last_digit = np.abs(output_signal_vector) % 10
    number_as_int = np.array([10 ** (n - i - 1) for i in range(n)]).dot(last_digit)
    return str(number_as_int).zfill(n)


def generate(i: int):
    while True:
        for value in [0, 1, 0, -1]:
            for _ in range(i + 1):
                yield value


@lru_cache(maxsize=5)
def matrix(n: int) -> np.ndarray:
    return np.array([
        list(islice(generate(i), n + 1))[1:]
        for i in range(n)
    ])


def digits(input_signal: str):
    return np.array([int(char) for char in input_signal])


def fft_x(signal: str, times: int) -> str:
    for _ in range(times):
        signal = fft(signal)
    return signal


class TestSilver(TestCase):
    def test_example0(self):
        self.assertEqual(
            fft_x('12345678', 1),
            '48226158'
        )
        self.assertEqual(
            fft_x('12345678', 4),
            '01029498'
        )

    def test_example1(self):
        self.assertEqual(
            fft_x('80871224585914546619083218645595', 100)[:8],
            '24176176'
        )

    def test_assignement(self):
        with open('data.txt') as file:
            data = file.readline()
        self.assertEqual(
            fft_x(data, 100)[:8],
            '69549155'
        )


# This solution is based on a couple of realizations:
# 1a) The input data is 651 digits long * 10_000 this makes for a 6_510_000 digit input
# 1b) The message_offset is 5_975_677
# 1c) message_offset >>> 6_510_000 / 2
# 1d) Thus the transition matrix is an upper triangular matrix of 1s (UT-1)
# 1e) So another way to formulate the problem is: ? = UT-1^100 * input
# 2) different rows in UT-1^N contain the same values except 1 shifted
# 3a) the values in 1 row of UT-1^2 are 1,2,3, ...
# 3b) the values in 1 row of UT-1^3 are 1,3,6, ...
# 3c) the values in 1 row of UT-1^4 are 1,4,10, ...
# 3d) This pattern is the cumsum(cumsum(...))
def solve_gold(data):
    message_offset = int(data[:7])
    data_expanded = data * 10_000
    data_selection = data_expanded[message_offset:]
    example = digits(data_selection)
    size = len(example)
    temp = np.ones((1, size))
    for _ in range(99):
        temp = np.cumsum(temp) % 10
    result = str(int(temp.dot(example) % 10))
    for i in range(1, 8):
        result += str(int(temp[:-i].dot(example[i:]) % 10))
    return result


class TestGold(TestCase):
    def test_example1(self):
        data = '03036732577212944063491565474664'
        self.assertEqual(
            solve_gold(data),
            '84462026'
        )

    def test_example3(self):
        data = '03081770884921959731165446850517'
        self.assertEqual(
            solve_gold(data),
            '53553731'
        )

    def test_assignement(self):
        with open('data.txt') as file:
            data = file.readline()
        self.assertEqual(
            solve_gold(data),
            '83253465'
        )
