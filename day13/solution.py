from unittest import TestCase

from shared.intcode import read_data, Intcode


class TestSilver(TestCase):
    def test_assignement(self):
        data = Intcode(read_data(), inputs=[]).run_program()
        self.assertEqual(
            sum(1 for type in data[2::3] if type == 2),
            268
        )


class TestGold(TestCase):
    def test_assignement(self):
        intcode = read_data()
        intcode[0] = 2
        data = Intcode(intcode, inputs=[]).run_program()
        state = [
            (data[i*3], data[i*3 + 1], data[i*3 + 2])
            for i in range(int(len(data) / 3))
        ]
        state.sort(key=lambda tile: (tile[1], tile[0]))
        max_x, max_y, _ = state[-1]
        for x, y, tile_id in state:
            if x == 0:
                print()
            if tile_id == 0:
                print('.', end='')
            elif tile_id == 1:
                print('#', end='')
            elif tile_id == 2:
                print('x', end='')
            elif tile_id == 3:
                print('-', end='')
            elif tile_id == 4:
                print('O', end='')
            else:
                print(int(tile_id), end='')
