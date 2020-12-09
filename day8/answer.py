from enum import Enum
from copy import deepcopy


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

    def switch_operation(self):
        if self.cmd == COMMAND_TYPES.JMP:
            return Command(f"{CMD_NOP} {self.num}")
        elif self.cmd == COMMAND_TYPES.NOP:
            return Command(f"{CMD_JMP} {self.num}")
        return Command(f"{CMD_ACC} {self.num}")

    def __str__(self):
        return f"{self.cmd} {self.num}"


with open("input", "r") as f:
    program = [Command(x) for x in f]


def execute_until_loop_or_end(program):
    stack_pointer = 0
    accumulator = 0
    seen_commands = set()
    while stack_pointer < len(program) and stack_pointer not in seen_commands:
        command = program[stack_pointer]
        seen_commands.add(stack_pointer)
        accumulator, stack_pointer = command.perform_operation(
            stack_pointer, accumulator
        )
    return (stack_pointer >= len(program), accumulator)


seen_commands = set()
stack_pointer = 0
accumulator = 0
while stack_pointer < len(program):
    command = program[stack_pointer]
    if stack_pointer in seen_commands:
        if command.cmd != COMMAND_TYPES.ACC:
            candidate_program = deepcopy(program)
            candidate_program[stack_pointer] = command.switch_operation()
            did_end, value = execute_until_loop_or_end(candidate_program)
            if did_end:
                print(f"{stack_pointer} {command} should be changed")
                accumulator = value
                break
    seen_commands.add(stack_pointer)
    accumulator, stack_pointer = command.perform_operation(stack_pointer, accumulator)
    # print(command)
    # print("accumulator", accumulator)
    # print("stack_pointer", stack_pointer)

print("Accumulator at termination", accumulator)
