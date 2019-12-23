from collections import defaultdict
from typing import List, Dict
from unittest import TestCase

from shared.intcode import read_data, Intcode


class Network:
    def __init__(self, num_computers: int, program: List[int]):
        self.computers = [
            Intcode(instructions=program.copy(), inputs=[i])
            for i in range(num_computers)
        ]
        self.packets: Dict[int, List[List[int]]] = defaultdict(lambda: [])

    def pop_packet(self, address: int) -> List[int]:
        packets = self.packets[address]
        if packets:
            return packets.pop(0)
        else:
            return [-1]

    def tick(self):
        packets = [
            self.pop_packet(address)
            for address in range(len(self.computers))
        ]
        for current_address, computer in enumerate(self.computers):
            print(f'computer {current_address:2} receiving: {packets[current_address]}')
            computer.add_input(packets[current_address])
            computer.run_program()
            for i in range(int(len(computer.output) / 3)):
                destination, x, y = computer.output[i * 3:i * 3 + 3]
                self.packets[destination].append([x, y])
                print(f'computer {current_address:2} sending: {computer.output[i * 3:i * 3 + 3]}')
            computer.output = []


def solve_silver() -> List[List[int]]:
    data = read_data()
    network = Network(num_computers=50, program=data)
    while not network.packets[255]:
        network.tick()
    return network.packets[255]


class TestSilver(TestCase):
    def test_assignement(self):
        self.assertListEqual(
            [[93889, 22650]],
            solve_silver()
        )
