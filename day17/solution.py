from unittest import TestCase

from shared.intcode import read_data, Intcode


def find_scafolds(output):
    return [
        i
        for i, x in enumerate(output)
        if x == 35
    ]


def find_intersections(scafolds, width):
    return [
        scafold
        for scafold in scafolds
        if (
                scafold - 1 in scafolds
                and
                scafold + 1 in scafolds
                and
                scafold - width in scafolds
                and
                scafold + width in scafolds
        )
    ]


def calc_alignement_parameters(intersections, width):
    return [
        (intersection % width) * int(intersection / width)
        for intersection in intersections
    ]


def solve_silver(output):
    width = output.index(10) + 1
    print(width)
    scafolds = find_scafolds(output)
    intersections = find_intersections(scafolds, width)
    alignement_parameters = calc_alignement_parameters(intersections, width)
    return sum(alignement_parameters)


class TestSilver(TestCase):
    # 6877 is too low
    # 7228 is too low
    def test_assignement(self):
        intcode = Intcode(read_data(), [])
        output = intcode.run_program()

        self.assertEqual(
            7328,
            solve_silver(output)
        )


# TODO: width assumed to be 58
NORTH = -58
EAST = -1
SOUTH = 58
WEST = 1
DIRECTIONS = [EAST, NORTH, SOUTH, WEST]

TURNS = {
    # (from, turn): to
    (NORTH, 'L'): EAST,
    (EAST, 'L'): SOUTH,
    (SOUTH, 'L'): WEST,
    (WEST, 'L'): NORTH,
    (EAST, 'R'): NORTH,
    (SOUTH, 'R'): EAST,
    (WEST, 'R'): SOUTH,
    (NORTH, 'R'): WEST,
}


def command_sequence(direction_robot, output, segments):
    scafolds = find_scafolds(output)
    robot = output.index(ord('^'))
    command = ''
    for _ in range(segments):
        turn_type = [
            turn_type
            for turn_type in ['L', 'R']
            if robot + TURNS[(direction_robot, turn_type)] in scafolds
        ][0]
        direction_robot = TURNS[(direction_robot, turn_type)]

        lenght_scafold = 1
        while robot + direction_robot * (lenght_scafold + 1) in scafolds:
            lenght_scafold += 1
        robot = robot + direction_robot * lenght_scafold

        command += turn_type + ',' + str(lenght_scafold) + ','
    return command[:-1]  # remove extra comma at the end


class TestGold(TestCase):
    # TODO: solutions based on facts from the assignement
    #  width assumed to be 58
    #  starting direction assumed to be ^
    #  segments count assumed to be 34
    #  determine sequences automatically
    def test_assignement(self, width=58, direction_robot=NORTH, segments=34):
        intcode = Intcode(read_data(), [])
        output = intcode.run_program()

        print(''.join([chr(char) for char in output]))

        command = command_sequence(direction_robot, output, segments)

        print(command)

        sequences = {
            'A': 'L,10,R,8,R,6,R,10',
            'B': 'L,12,R,8,L,12',
            'C': 'L,10,R,8,R,8'
        }
        for function, sequence in sequences.items():
            command = command.replace(sequence, function)

        full_input = command + '\n' + sequences['A'] + '\n' + sequences['B'] + '\n' + sequences['C'] + '\n' + 'n' + '\n'
        print(full_input)

        input_commands = [
            ord(char)
            for char in full_input
        ]

        print(input_commands)

        data = read_data()
        data[0] = 2
        intcode = Intcode(data, input_commands)
        output = intcode.run_program()

        # print(''.join([chr(char) for char in output]))

        self.assertEqual(
            output[-1],
            1289413
        )
