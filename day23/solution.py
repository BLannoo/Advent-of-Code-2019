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
        self.rounds_idle = 0
        self.nat_delivered_packets = []

    def pop_packet(self, address: int) -> List[int]:
        packets = self.packets[address]
        if packets:
            return packets.pop(0)
        else:
            return [-1]

    def tick(self):
        packets = self.pop_packets()
        for current_address in range(len(self.computers)):
            self.computers[current_address].add_input(packets[current_address])

        for current_address in range(len(self.computers)):
            self.computers[current_address].run_program()

        had_output = False
        for current_address in range(len(self.computers)):
            for i in range(int(len(self.computers[current_address].output) / 3)):
                had_output = True
                destination, x, y = self.computers[current_address].output[i * 3:i * 3 + 3]
                self.packets[destination].append([x, y])
                if destination >= len(self.computers):
                    print(
                        f'computer {current_address:2} sending [{x}, {y}] to {destination}')
            self.computers[current_address].output = []

        # if was idle
        if any([packet != [-1] for packet in packets]) == 0 and not had_output:
            if self.rounds_idle >= 5:
                nat_packet = self.packets[255][-1]
                self.packets[0].append(nat_packet)
                self.nat_delivered_packets.append(nat_packet)
                self.rounds_idle = 0
            else:
                self.rounds_idle += 1

    def pop_packets(self):
        return [self.pop_packet(address) for address in range(len(self.computers))]


def solve_silver() -> List[List[int]]:
    data = read_data()
    network = Network(num_computers=50, program=data)
    while not network.packets[255]:
        network.tick()
    return network.packets[255]


def solve_gold() -> List[int]:
    data = read_data()
    network = Network(num_computers=50, program=data)
    # for _ in range(1000):
    while len(network.nat_delivered_packets) < 2 or (network.nat_delivered_packets[-1] != network.nat_delivered_packets[-2]):
        network.tick()

    print([
        y
        for x, y in network.packets[255]
    ])
    print([
        y
        for x, y in network.nat_delivered_packets
    ])
    return network.nat_delivered_packets[-1]


class TestSilver(TestCase):
    def test_assignement(self):
        self.assertListEqual(
            [[93889, 22650]],
            solve_silver()
        )


class TestGold(TestCase):
    # not twice in a row:
    # 17363 is too high
    #
    # not delivered, but stored:
    # 17300 is too high
    #
    # 17200 is too low (random guess)
    # 17292 is wrong (random guess)
    def test_assignement(self):
        self.assertListEqual(
            [93889, 17298],
            solve_gold()
        )
