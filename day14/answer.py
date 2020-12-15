from enum import Enum
import re


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


if __name__ == "__main__":
    instructions = get_instructions()
    print("Part 1: ", part_1(instructions))
