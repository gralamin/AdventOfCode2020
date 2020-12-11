min_voltage_modifier = 3

max_of_all_voltage_modifer = 3

with open("input", "r") as f:
    jolts = [int(x) for x in f if x != "\n"]

differences = {}

sorted_jolts = sorted(jolts)
sorted_jolts.append(sorted_jolts[-1] + max_of_all_voltage_modifer)

cur_joltage = 0
for j in sorted_jolts:
    if j - min_voltage_modifier > cur_joltage:
        raise ValueError("impossible")
    difference = j - cur_joltage
    differences[difference] = differences.setdefault(difference, 0) + 1
    cur_joltage = j

print("Part 1: ", differences[1] * differences[3])
