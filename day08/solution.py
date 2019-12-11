from unittest import TestCase

from shared.ocr import ocr


def read_data():
    with open('data.txt') as file:
        return file.read()


def solve_silver(data, wide, tall):
    layers = slice_layers(data, tall, wide)
    layer_with_fewest_zeros = min(layers, key=lambda layer: layer.count('0'))
    return layer_with_fewest_zeros.count('1') * layer_with_fewest_zeros.count('2')


def solve_gold(data, wide, tall):
    layers = slice_layers(data, tall, wide)
    return [
        [
            determine_pixel(layers, x, y, wide)
            for x in range(wide)
        ]
        for y in range(tall)
    ]


def determine_pixel(layers, x, y, wide):
    for layer in layers:
        pixel = layer[x + wide * y]
        if pixel != '2':
            return int(pixel) * -1


def slice_layers(data, tall, wide):
    layer_size = wide * tall
    num_layers = int(len(data) / layer_size)
    layers = [
        data[i * layer_size:(i + 1) * layer_size]
        for i in range(num_layers)
    ]
    return layers


class TestSilver(TestCase):
    def test_example_0(self):
        self.assertEqual(
            solve_silver('123456789012', wide=3, tall=2),
            1
        )

    # 1584 is to low (missing last pixel on every layer)
    def test_assignement(self):
        self.assertEqual(
            solve_silver(read_data(), wide=25, tall=6),
            1596
        )


class TestGold(TestCase):
    def test_assignement(self):
        image = solve_gold(read_data(), wide=25, tall=6)
        self.assertEqual(
            ocr(image),
            'LBRCE'
        )
