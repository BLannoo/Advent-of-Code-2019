from unittest import TestCase

translation = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


def follow(direction, starting_point):
    move = translation[direction[0]]
    return [
        (starting_point[0] + move[0] * i, starting_point[1] + move[1] * i)
        for i in range(1, int(direction[1:]) + 1)
    ]


def execute_directions(directions):
    path = [(0, 0)]
    for direction in directions:
        path.extend(follow(direction, path[-1]))
    return path


def find_closest(path1, path2):
    intersections = set(path1).intersection(path2)
    return min([
        abs(intersection[0]) + abs(intersection[1])
        for intersection in intersections
        if intersection != (0, 0)
    ])


class Test(TestCase):
    def test_example_0(self):
        self.assertEqual(
            6,
            find_closest(
                execute_directions(['R8', 'U5', 'L5', 'D3']),
                execute_directions(['U7', 'R6', 'D4', 'L4'])
            )
        )

    def test_example_1(self):
        self.assertEqual(
            159,
            find_closest(
                execute_directions(['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']),
                execute_directions(['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'])
            )
        )

    def test_assignement_1(self):
        with open('data.txt') as file:
            directions1 = file.readline().split(',')
            directions2 = file.readline().split(',')
        self.assertEqual(
            489,
            find_closest(
                execute_directions(directions1),
                execute_directions(directions2)
            )
        )

    def test_assignement_2(self):
        with open('data.txt') as file:
            directions1 = file.readline().split(',')
            directions2 = file.readline().split(',')
        path1 = execute_directions(directions1)
        path2 = execute_directions(directions2)
        intersections = set(path1).intersection(set(path2))
        self.assertEqual(
            93654,
            min([
                path1.index(intersection) + path2.index(intersection)
                for intersection in intersections
                if intersection != (0, 0)
            ])
        )
