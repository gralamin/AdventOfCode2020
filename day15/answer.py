import time


def get_input():
    with open("input", "r") as f:
        numbers = [int(x) for x in f.read().strip().split(",")]
    return numbers


def van_eck_with_start_state(start_state, turns):
    seen = {number: i + 1 for i, number in enumerate(start_state)}
    value = 0
    turn_offset = len(start_state) + 1
    for x in range(turns - turn_offset):
        yield value
        offset_turn = x + turn_offset
        # print(f"{offset_turn}: {value}, {seen}")
        last = {value: offset_turn}
        new_value = offset_turn - seen.get(value, offset_turn)
        seen[value] = last[value]
        value = new_value
    yield value


def part_1(numbers):
    # This is a Van Eck Sequence
    start = time.perf_counter()
    result = list(van_eck_with_start_state(numbers, 2020))[-1]
    end = time.perf_counter()
    print("P1 Runtime: {:.3f}".format(end - start))
    return result


def part_2(numbers):
    # This is a Van Eck Sequence
    start = time.perf_counter()
    result = list(van_eck_with_start_state(numbers, 30000000))[-1]
    end = time.perf_counter()
    print("P2 Runtime: {:.3f}".format(end - start))
    return result


if __name__ == "__main__":
    numbers = get_input()
    print(numbers)
    print(f"Part 1: '{part_1(numbers)}'")
    print(f"Part 2: '{part_2(numbers)}'")
