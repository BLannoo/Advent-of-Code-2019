from unittest import TestCase


def read_input():
    with open('data.txt') as file:
        return [
            int(code)
            for code in file.readline().split(',')
        ]


opcodes = {
    1: (lambda intcode: intcode.opcode_1_2(lambda a, b: a + b)),
    2: (lambda intcode: intcode.opcode_1_2(lambda a, b: a * b)),
    99: (lambda intcode: intcode.opcode_99()),
}


class Intcode:
    def __init__(self, instructions):
        self.__instructions = instructions
        self.__pointer = 0
        self.__halted = False

    def run_program(self):
        while not self.__halted:
            opcode = self.__instructions[self.__pointer]
            opcodes[opcode](self)
        return self.__instructions[0]

    def opcode_1_2(self, combinator):
        input1 = self.__instructions[self.__instructions[self.__pointer + 1]]
        input2 = self.__instructions[self.__instructions[self.__pointer + 2]]
        result = combinator(input1, input2)
        output = self.__instructions[self.__pointer + 3]
        self.__instructions[output] = result
        self.__pointer += 4

    def opcode_99(self):
        self.__halted = True


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
