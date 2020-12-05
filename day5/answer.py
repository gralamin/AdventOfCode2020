from enum import Enum

# No need to round, 128 is a power of 2, always divides evenly until 1.
rows_min = 0
rows_max = 127

col_min = 0
col_max = 7

INPUT_FRONT = "F"
INPUT_BACK = "B"
INPUT_LEFT = "L"
INPUT_RIGHT = "R"


class SpacePartition(Enum):
    towards_max = 0
    towards_min = 1

    @classmethod
    def get_by_input_str(cls, input_char):
        if input_char in [INPUT_FRONT, INPUT_LEFT]:
            return cls.towards_min
        if input_char in [INPUT_RIGHT, INPUT_BACK]:
            return cls.towards_max
        raise ValueError(f"Unknown input {input_char}")


# Example run of this recursive function:
# 0, 127, FBFBBFB
# F -> Towards min, 0, 63, BFBBFB
# B -> Towards max, 32, 63, FBBFB
# F -> Towards min, half is 47. 32, 47, BBFB
# B -> Towards max, half is 39. 40, 47, BFB
# B -> Towards max, half is 43. 44, 47, FB
# F -> Towards min, half is 45. 44, 45, B
# B -> Towards max, half is 44. 45, 45, ""
# Matches, return 45.
def binary_partition(cur_min, cur_max, remaining_input):
    # print(f"#DEBUG: {cur_min}, {cur_max}, {remaining_input}")
    if cur_min == cur_max:
        return cur_min
    elif cur_min > cur_max:
        raise ValueError("Min has exceeded max")
    cur_input = remaining_input[0]
    next_input = remaining_input[1:]
    # half starts at 0 + 127 -> 127 / 2 = 63. We want to add 1
    # if moving towards the max, as this is actually the lower
    # half way point.
    # Use // to integer divide.
    half = (cur_min + cur_max) // 2
    direction = SpacePartition.get_by_input_str(cur_input)
    if direction == SpacePartition.towards_max:
        return binary_partition(half + 1, cur_max, next_input)
    else:
        return binary_partition(cur_min, half, next_input)


class BoardingPass:
    def __init__(self, input_str):
        row_str = input_str[0:7]
        col_str = input_str[7:]
        self.row = binary_partition(rows_min, rows_max, row_str)
        self.col = binary_partition(col_min, col_max, col_str)

    def get_seat_id(self):
        return self.row * 8 + self.col


with open("input", "r") as f:
    boarding_passes = [BoardingPass(x.strip()) for x in f]
results = [b.get_seat_id() for b in boarding_passes]

print(f"Top result {max(results)}")
