from enum import Enum
from collections import deque
import time


class MATH_SYMBOLS(Enum):
    ADDITION = 1
    MULTIPLICATION = 2
    OPEN_BRACKET = 3
    CLOSED_BRACKET = 4


class MathEvaluator:
    def __init__(self, precedence_plus=1, precedence_multiply=1):
        self.precedence_plus = precedence_plus
        self.precedence_multiply = precedence_multiply

    def evaluate(self, expression):
        lexed = self._lex(expression)
        reverse_polish = self._shunting_yard(lexed)
        stack = []
        # print(reverse_polish)
        for x in reverse_polish:
            # print(x, stack)
            if x == MATH_SYMBOLS.ADDITION:
                op1 = stack.pop()
                op2 = stack.pop()
                stack.append(op1 + op2)
            elif x == MATH_SYMBOLS.MULTIPLICATION:
                op1 = stack.pop()
                op2 = stack.pop()
                stack.append(op1 * op2)
            else:
                stack.append(x)
        # print(stack)
        if len(stack) > 1:
            raise ValueError("More than one result in stack at end")
        return stack[0]

    def _lex(self, expression):
        # Convert to easy to use tokens
        lexed = []
        split = expression.strip().split(" ")
        for x in split:
            to_add_end = 0
            while "(" in x:
                lexed.append(MATH_SYMBOLS.OPEN_BRACKET)
                x = x[1:]
            if "+" in x:
                lexed.append(MATH_SYMBOLS.ADDITION)
                continue
            elif "*" in x:
                lexed.append(MATH_SYMBOLS.MULTIPLICATION)
                continue
            while ")" in x:
                to_add_end += 1
                x = x[:-1]
            lexed.append(int(x))
            for _ in range(to_add_end):
                lexed.append(MATH_SYMBOLS.CLOSED_BRACKET)
        return lexed

    def _get_precedence(self, symbol):
        if symbol == MATH_SYMBOLS.ADDITION:
            return self.precedence_plus
        elif symbol == MATH_SYMBOLS.MULTIPLICATION:
            return self.precedence_multiply
        else:
            raise ValueError(f"Trying to get precedence of {symbol}")

    def _shunting_yard(self, lexed):
        stack = []
        output = deque()
        for x in lexed:
            if x == MATH_SYMBOLS.ADDITION:
                while len(stack) > 0 and stack[-1] != MATH_SYMBOLS.OPEN_BRACKET:
                    precendence_x = self._get_precedence(x)
                    precendence_top = self._get_precedence(stack[-1])
                    if precendence_x <= precendence_top:
                        output.append(stack.pop())
                    else:
                        break
                stack.append(x)
            elif x == MATH_SYMBOLS.MULTIPLICATION:
                while len(stack) > 0 and stack[-1] != MATH_SYMBOLS.OPEN_BRACKET:
                    precendence_x = self._get_precedence(x)
                    precendence_top = self._get_precedence(stack[-1])
                    if precendence_x <= precendence_top:
                        output.append(stack.pop())
                    else:
                        break
                stack.append(x)
            elif x == MATH_SYMBOLS.OPEN_BRACKET:
                stack.append(MATH_SYMBOLS.OPEN_BRACKET)
            elif x == MATH_SYMBOLS.CLOSED_BRACKET:
                to_output = None
                while to_output != MATH_SYMBOLS.OPEN_BRACKET:
                    if to_output:
                        output.append(to_output)
                    to_output = stack.pop()
            else:
                output.append(x)
        while len(stack) > 0:
            output.append(stack.pop())
        return output


def get_input():
    expressions = []
    with open("input", "r") as f:
        for x in f:
            x = x.strip()
            if x:
                expressions.append(x)
    return expressions


def part1(input_value):
    evaluator = MathEvaluator(precedence_plus=1, precedence_multiply=1)
    results = [evaluator.evaluate(x) for x in input_value]
    return sum(results)


def part2(input_value):
    evaluator = MathEvaluator(precedence_plus=2, precedence_multiply=1)
    results = [evaluator.evaluate(x) for x in input_value]
    return sum(results)


if __name__ == "__main__":
    expressions = get_input()
    start = time.perf_counter()
    print("Part1:", part1(expressions))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
    start = time.perf_counter()
    print("Part 2:", part2(expressions))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
