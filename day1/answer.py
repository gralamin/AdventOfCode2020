

INPUT_FILENAME = "input_1"

inputs = []

with open(INPUT_FILENAME, "r") as f:
    inputs = [int(x) for x in f]

inputs = sorted(inputs)

def find_values_matching(result, inputs):
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

results = set()
for (x, y) in find_values_matching(2020, inputs):
    results.add((x, y))

for r in results:
    print(r[0] * r[1])


