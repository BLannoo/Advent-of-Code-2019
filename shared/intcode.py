def read_input():
    with open('data.txt') as file:
        return [
            int(code)
            for code in file.readline().split(',')
        ]


opcodes = {
    1: (lambda intcode: intcode.opcode_1_2(lambda a, b: a + b)),
    2: (lambda intcode: intcode.opcode_1_2(lambda a, b: a * b)),
    3: (lambda intcode: intcode.opcode_3()),
    4: (lambda intcode: intcode.opcode_4()),
    5: (lambda intcode: intcode.opcode_5_6(lambda a: a != 0)),
    6: (lambda intcode: intcode.opcode_5_6(lambda a: a == 0)),
    7: (lambda intcode: intcode.opcode_7_8(lambda a, b: a < b)),
    8: (lambda intcode: intcode.opcode_7_8(lambda a, b: a == b)),
    99: (lambda intcode: intcode.opcode_99()),
}


class Intcode:
    def __init__(self, instructions, input=0):
        self.__instructions = instructions
        self.__input = input
        self.output = []
        self.__pointer = 0
        self.__halted = False

    def run_program(self):
        while not self.__halted:
            opcodes[self.opcode()](self)
            # print(self.__instructions, self.__pointer)
        if len(self.output) == 0:
            return self.__instructions[0]
        else:
            return self.output

    def opcode(self):
        return self.__instructions[self.__pointer] % 100

    def get_input(self, shift):
        if int(self.__instructions[self.__pointer] / (10 * 10**shift)) % 10 == 1:
            return self.__instructions[self.__pointer + shift]
        return self.__instructions[self.__instructions[self.__pointer + shift]]

    def opcode_1_2(self, combinator):
        input1 = self.get_input(1)
        input2 = self.get_input(2)
        result = combinator(input1, input2)
        output = self.__instructions[self.__pointer + 3]
        self.__instructions[output] = result
        self.__pointer += 4

    def opcode_3(self):
        location = self.__instructions[self.__pointer + 1]
        self.__instructions[location] = self.__input
        self.__pointer += 2

    def opcode_4(self):
        self.output.append(self.get_input(1))
        self.__pointer += 2

    def opcode_5_6(self, evaluator):
        input1 = self.get_input(1)
        if evaluator(input1):
            self.__pointer = self.get_input(2)
        else:
            self.__pointer += 3

    def opcode_7_8(self, comparator):
        input1 = self.get_input(1)
        input2 = self.get_input(2)
        output = self.__instructions[self.__pointer + 3]
        if comparator(input1, input2):
            self.__instructions[output] = 1
        else:
            self.__instructions[output] = 0
        self.__pointer += 4

    def opcode_99(self):
        self.__halted = True
