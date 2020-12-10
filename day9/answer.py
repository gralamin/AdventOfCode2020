int_values = []

with open("input", "r") as f:
    int_values = [int(x) for x in f]


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


def find_first_not_sum(int_values):
    for index, value in enumerate(int_values):
        if index < 25:
            # 25 line preamble
            continue
        low_index = index - 25
        last_numbers = int_values[low_index:index]
        for _ in find_values_matching(value, last_numbers):
            break
        else:
            # yielded no results (otherwise break would be called)
            # so no sum
            return index, value


x, y = find_first_not_sum(int_values)
print("At index", x, " - ", y)
