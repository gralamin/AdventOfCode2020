from functools import reduce


def get_input():
    start_timestamp = 0
    buses = []

    with open("input", "r") as f:
        start_timestamp = int(f.readline())
        buses = f.readline().strip().split(",")
    return start_timestamp, buses


def part_1(start_timestamp, buses):
    lowest_wait = start_timestamp + 1
    lowest_bus = None
    for bus in buses:
        if bus == "x":
            continue
        # If we are at 9 minutes, and bus comes every 10, then wait time will be 1.
        # This is the value, subtracted by mod, all moded again so 0 case ends ups
        # as 0.
        bus = int(bus)
        wait_time = (bus - (start_timestamp % bus)) % bus
        # print(f"For bus {bus}, wait is {wait_time}")
        lowest_wait = min(lowest_wait, wait_time)
        if lowest_wait == wait_time:
            lowest_bus = int(bus)
    return lowest_wait * lowest_bus


def chinese_remainder(n, a):
    # Implementation stolen from Rosetta Code.
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def part_2(buses):
    # This is the "Chinese remainder Theorem"
    bus_indexes = [(i, int(bus)) for i, bus in enumerate(buses) if bus != "x"]
    divisors = [bus for _, bus in bus_indexes]
    remainders = [bus - i for i, bus in bus_indexes]
    return chinese_remainder(divisors, remainders)


if __name__ == "__main__":
    START, BUSES = get_input()
    print("Part 1:", part_1(START, BUSES))
    print("Part 2:", part_2(BUSES))
