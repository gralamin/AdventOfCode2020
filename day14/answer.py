from enum import Enum
import re
import time


class InstructionType(Enum):
    MASK = 1
    MEM = 2


# Define: MASK = 12321 Type is mask, arg1 gets set to None, arg2 gets set to 12321.
# Define: Mem[12] = 52 Type is mem, arg1 gets set to 12, arg2 gets ste to 52
class Instruction:
    def __init__(self, ins_type, arg1, arg2):
        self.ins_type = ins_type
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        return f"{self.ins_type} {self.arg1} {self.arg2}"

    @classmethod
    def from_input(cls, input_str):
        lhs, rhs = input_str.split("=")
        arg2 = rhs.strip()
        arg1 = None
        if lhs.startswith("mem"):
            ins_type = InstructionType.MEM
            extract = re.search("mem\\[(\\d+)\\]", lhs)
            if extract:
                arg1 = int(extract.groups()[0])
            else:
                raise ValueError(f"Cannot parse {input_str}")
            arg2 = int(arg2)
        elif lhs.startswith("mask"):
            ins_type = InstructionType.MASK
        else:
            raise ValueError("Unknown instruction")
        return cls(ins_type, arg1, arg2)


class BitMask:
    def __init__(self):
        self.mask = ["X"] * 36

    def set_mask(self, some_str):
        self.mask = list(some_str)

    def mask_value(self, value):
        value_as_binary_list = (["0"] * 36) + list("{0:b}".format(value))
        value_as_binary_list = value_as_binary_list[-36:]
        for index, mask_bit in enumerate(self.mask):
            if mask_bit == "X":
                continue
            value_as_binary_list[index] = mask_bit
        return int("".join(value_as_binary_list), 2)

    def mask_possible_addresses(self, address):
        value_as_binary_list = (["0"] * 36) + list("{0:b}".format(address))
        value_as_binary_list = value_as_binary_list[-36:]
        floating_positions = []
        for index, mask_bit in enumerate(self.mask):
            if mask_bit == "0":
                continue
            elif mask_bit == "1":
                value_as_binary_list[index] = mask_bit
            elif mask_bit == "X":
                value_as_binary_list[index] = "F"
                floating_positions.append(index)

        # Make a list of all possible mask bits
        possible_combinations = []
        for x in range(2 ** len(floating_positions)):
            as_binary = list("{0:b}".format(x))
            as_binary = ["0"] * (len(floating_positions) - len(as_binary)) + as_binary
            possible_combinations.append(as_binary)

        for x in possible_combinations:
            for floating_index, value_index in enumerate(floating_positions):
                value_as_binary_list[value_index] = x[floating_index]
            yield int("".join(value_as_binary_list), 2)


class Memory:
    def __init__(self):
        self.memory_addresses = {}

    def set_address(self, address, modified_value):
        self.memory_addresses[address] = modified_value

    def get_sum(self):
        return sum(self.memory_addresses.values())


class ComputerState:
    def __init__(self):
        self.mask = BitMask()
        self.memory = Memory()

    def do_instruction(self, instruction):
        if instruction.ins_type == InstructionType.MASK:
            self.mask.set_mask(instruction.arg2)
        elif instruction.ins_type == InstructionType.MEM:
            masked_value = self.mask.mask_value(instruction.arg2)
            self.memory.set_address(instruction.arg1, masked_value)
        else:
            raise ValueError("Unknown instruction")

    def do_instruction2(self, instruction):
        if instruction.ins_type == InstructionType.MASK:
            self.mask.set_mask(instruction.arg2)
        elif instruction.ins_type == InstructionType.MEM:
            for address in self.mask.mask_possible_addresses(instruction.arg1):
                self.memory.set_address(address, instruction.arg2)
        else:
            raise ValueError("Unknown instruction")

    def get_sum(self):
        return self.memory.get_sum()


def get_instructions():
    with open("input", "r") as f:
        return [Instruction.from_input(x) for x in f if x.strip() != ""]


def part_1(input_instructions):
    state = ComputerState()
    for instruction in input_instructions:
        state.do_instruction(instruction)
    return state.get_sum()


def part_2(input_instructions):
    state = ComputerState()
    for instruction in input_instructions:
        state.do_instruction2(instruction)
    return state.get_sum()


if __name__ == "__main__":
    start = time.perf_counter()
    instructions = get_instructions()
    print("Part 1: ", part_1(instructions))
    print("Part 2: ", part_2(instructions))
    end = time.perf_counter()
    print("Runtime: {:.3f}".format(end-start))
