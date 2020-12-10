int_values = []

SIZE = 25
INPUT = "input"

# SIZE = 5
# INPUT = "input_sample"

with open(INPUT, "r") as f:
    int_values = [int(x) for x in f if x != "\n"]


def find_values_matching(result, inputs):
    inputs = sorted(inputs)
    for x in inputs:
        for y in inputs:
            if x == y:
                continue
            total = x + y
            if total > result:
                break
            if total == result:
                if x > y:
                    yield x, y
                else:
                    yield y, x


def find_contiguous_numbers(result, inputs):
    for index, x in enumerate(inputs):
        # print("\n\n=========")
        previous_nums = inputs[:index]
        # Walk backwards in the set until we equal or exceed.
        # Backwards and forwards are both pretty do-able, but I find the backwards
        # a bit more intuitive
        cur_result = result - x
        top_index = len(previous_nums) - 1
        # print(f"Checking {x}, curValue {cur_result}")
        while top_index > 0:
            cur_result -= inputs[top_index]
            # print(f"next is {inputs[top_index]}, curValue {cur_result}")
            if cur_result == 0:
                return inputs[top_index:index]
            if cur_result < 0:
                break
            top_index -= 1
    raise ValueError("Failed to find")


def find_first_not_sum(int_values):
    for index, value in enumerate(int_values):
        if index < SIZE:
            # 25 line preamble
            continue
        low_index = index - SIZE
        last_numbers = int_values[low_index:index]
        for _ in find_values_matching(value, last_numbers):
            break
        else:
            # yielded no results (otherwise break would be called)
            # so no sum
            return index, value


x, y = find_first_not_sum(int_values)
print("At index", x, " - ", y)

contiguous_set = find_contiguous_numbers(y, int_values)
print("Encryption weakness", min(contiguous_set) + max(contiguous_set))
