from collections import defaultdict
from copy import copy
from typing import List


def read_data() -> List[int]:
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
    9: (lambda intcode: intcode.opcode_9()),
    99: (lambda intcode: intcode.opcode_99()),
}


class Intcode:
    def __init__(self, instructions, inputs=[0]):
        self.__instructions = copy(instructions)
        self.__extra_instructions = defaultdict(lambda: 0)
        self.__inputs = inputs
        self.__input_pointer = 0
        self.output = []
        self.__pointer = 0
        self.input_required = False
        self.halted = False
        self.relative_base = 0

    def run_program(self):
        while not self.halted and not self.input_required:
            opcode = self.opcode()
            opcodes[opcode](self)
            # print(self.__instructions, self.__pointer)
        if len(self.output) == 0:
            return self.get_instruction(0)
        else:
            return self.output

    def add_input(self, values):
        self.__inputs.extend(values)
        self.input_required = False

    def opcode(self):
        return self.get_instruction(self.__pointer) % 100

    def get_parameter(self, shift):
        location = self.location_memory_access(shift)
        return self.get_instruction(location)

    def location_memory_access(self, shift):
        mode = int(self.get_instruction(self.__pointer) / (10 * 10 ** shift)) % 10
        if mode == 1:
            location = self.__pointer + shift
        elif mode == 2:
            location = self.get_instruction(self.__pointer + shift) + self.relative_base
        elif mode == 0:
            location = self.get_instruction(self.__pointer + shift)
        else:
            raise Exception('non existing mode was called, mode was: {}'.format(mode))
        return location

    def get_instruction(self, position):
        if position >= len(self.__instructions):
            return self.__extra_instructions[position]
        return self.__instructions[position]

    def set_instruction(self, position, value):
        if position >= len(self.__instructions):
            self.__extra_instructions[position] = value
        else:
            self.__instructions[position] = value

    def opcode_1_2(self, combinator):
        input1 = self.get_parameter(1)
        input2 = self.get_parameter(2)
        result = combinator(input1, input2)
        output = self.location_memory_access(3)
        self.set_instruction(output, result)
        self.__pointer += 4

    def opcode_3(self):
        if self.__input_pointer >= len(self.__inputs):
            self.input_required = True
            return
        location = self.location_memory_access(1)
        self.set_instruction(location,  self.__inputs[self.__input_pointer])
        self.__input_pointer += 1
        self.__pointer += 2

    def opcode_4(self):
        self.output.append(self.get_parameter(1))
        self.__pointer += 2

    def opcode_5_6(self, evaluator):
        input1 = self.get_parameter(1)
        if evaluator(input1):
            self.__pointer = self.get_parameter(2)
        else:
            self.__pointer += 3

    def opcode_7_8(self, comparator):
        input1 = self.get_parameter(1)
        input2 = self.get_parameter(2)
        output = self.location_memory_access(3)
        if comparator(input1, input2):
            self.set_instruction(output, 1)
        else:
            self.set_instruction(output, 0)
        self.__pointer += 4

    def opcode_9(self):
        parameter = self.get_parameter(1)
        self.relative_base += parameter
        self.__pointer += 2

    def opcode_99(self):
        self.halted = True
