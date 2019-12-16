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
