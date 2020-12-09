from enum import Enum


class COMMAND_TYPES(Enum):
    NOP = 1
    ACC = 2
    JMP = 3


CMD_NOP = "nop"
CMD_ACC = "acc"
CMD_JMP = "jmp"


class Command:
    def __init__(self, assembly_str):
        split_str = assembly_str.split(" ")
        raw_cmd = split_str[0].strip()
        cmd = None
        if raw_cmd == CMD_NOP:
            cmd = COMMAND_TYPES.NOP
        elif raw_cmd == CMD_ACC:
            cmd = COMMAND_TYPES.ACC
        elif raw_cmd == CMD_JMP:
            cmd = COMMAND_TYPES.JMP
        else:
            raise Exception("Unknown input")
        self.cmd = cmd
        self.num = int(split_str[1].strip())

    def perform_operation(self, stack_pointer, accumulator):
        if self.cmd == COMMAND_TYPES.ACC:
            accumulator += self.num
            stack_pointer += 1
        if self.cmd == COMMAND_TYPES.JMP:
            stack_pointer += self.num
        if self.cmd == COMMAND_TYPES.NOP:
            stack_pointer += 1
        return (accumulator, stack_pointer)

    def __str__(self):
        return f"{self.cmd} {self.num}"


with open("input", "r") as f:
    program = [Command(x) for x in f]

seen_commands = set()

stack_pointer = 0
accumulator = 0
while stack_pointer not in seen_commands:
    seen_commands.add(stack_pointer)
    command = program[stack_pointer]
    accumulator, stack_pointer = command.perform_operation(stack_pointer, accumulator)
    # print(command)
    # print("accumulator", accumulator)
    # print("stack_pointer", stack_pointer)

print("Accumulator before loop", accumulator)
