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


if __name__ == "__main__":
    START, BUSES = get_input()
    print("Part 1:", part_1(START, BUSES))
