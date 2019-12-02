def read_input():
    with open('data.txt') as file:
        return [
            int(code)
            for code in file.readline().split(',')
        ]


def execute(intcode, position):
    # print('executing position: ', position)
    opcode = intcode[position]
    # print('opcode is: ', opcode)
    input1 = intcode[intcode[position + 1]]
    # print('input1 is: ', input1)
    input2 = intcode[intcode[position + 2]]
    # print('input2 is: ', input2)
    if opcode == 1:
        result = input1 + input2
    if opcode == 2:
        result = input1 * input2
    # print('result is:', result)
    output = intcode[position + 3]
    # print('output is:', output)
    intcode[output] = result
    # print('this results in: ', intcode)


def run_program(input):
    i = 0
    while input[i] != 99:
        execute(input, i)
        i += 4
    # print('found 99: ', input[0])
    return input[0]


print('example 0: ', run_program([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]))

data = read_input()
data[1] = 12
data[2] = 2
print('assignment 1: ', run_program(data))

for noun in range(100):
    for verb in range(100):
        data = read_input()
        data[1] = noun
        data[2] = verb
        if run_program(data) == 19690720:
            print('solution found (', 100 * noun + verb, '): noun=', noun, ' and verb=', verb)
