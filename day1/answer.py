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

def solve_1():
    results = set()
    for (x, y) in find_values_matching(2020, inputs):
        results.add((x, y))

    print("Solutions 1")
    for r in results:
        print(r[0] * r[1])

def solve_2():
    results = set()
    for z in inputs:
        for (x, y) in find_values_matching(2020-z, inputs):
            if x == z or y == z:
                continue
            results.add(tuple(sorted([x,y,z])))

    print("Solutions 2")
    for r in results:
        print(r[0] * r[1] * r[2])

solve_1()
solve_2()


