min_voltage_modifier = 3

max_of_all_voltage_modifer = 3

with open("input", "r") as f:
    jolts = [int(x) for x in f if x != "\n"]

differences = {}

sorted_jolts = sorted(jolts)
device = sorted_jolts[-1] + max_of_all_voltage_modifer
sorted_jolts.append(device)

cur_joltage = 0
for j in sorted_jolts:
    if j - min_voltage_modifier > cur_joltage:
        raise ValueError("impossible")
    difference = j - cur_joltage
    differences[difference] = differences.setdefault(difference, 0) + 1
    cur_joltage = j

print("Part 1: ", differences[1] * differences[3])

# Part 2 is a bit more complex...
# Easiest solution I can think of is building a graph.


def graph(inputs):
    neighbors = {}
    # O(n^2), because for each value, we look in the list for another value.
    for j in inputs:
        potential_neighbors = [j + x for x in [1, 2, 3]]
        neighbors[j] = [n for n in potential_neighbors if n in inputs]
    return neighbors


# Add 0 base state for graph
sorted_jolts = [0] + sorted_jolts
paths = graph(sorted_jolts)

# Now, count the paths
# We have 1 way to get to 0, as its our start.
counted_paths = {0: 1}
for j, neighbors in paths.items():
    for n in neighbors:
        counted_paths[n] = counted_paths.setdefault(n, 0) + counted_paths[j]

# Then check how many are at the device
print("Part 2", counted_paths[device])
