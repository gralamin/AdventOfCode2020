FLOOR = "."
EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"

with open("input", "r") as f:
    map = [[y for y in x.strip()] for x in f]


def get_adjacents(old_map, x, y):
    adjacents = []
    top_edge = x == 0
    bottom_edge = x + 1 == len(old_map)
    left_edge = y == 0
    right_edge = y + 1 == len(old_map[0])

    if not top_edge:
        # Diagonal Up Left
        if not left_edge:
            adjacents.append(old_map[x - 1][y - 1])
        # Up
        adjacents.append(old_map[x - 1][y])
        # Diagonal Up Right
        if not right_edge:
            adjacents.append(old_map[x - 1][y + 1])
    if not left_edge:
        # Left
        adjacents.append(old_map[x][y - 1])
    if not right_edge:
        # Right
        adjacents.append(old_map[x][y + 1])
    if not bottom_edge:
        # Diagonal bottom left
        if not left_edge:
            adjacents.append(old_map[x + 1][y - 1])
        # Down
        adjacents.append(old_map[x + 1][y])
        # Bottom right
        if not right_edge:
            adjacents.append(old_map[x + 1][y + 1])
    return adjacents


def calc_new_map(old_map, adjacent_method=get_adjacents, num_occupied_to_be_empty=4):
    new_map = [[] for _ in old_map]
    state_changed = False
    for x, row in enumerate(old_map):
        for y, col in enumerate(row):
            new_state = col
            if col == FLOOR:
                new_map[x].append(new_state)
                continue
            adjacents = adjacent_method(old_map, x, y)
            if col == EMPTY_SEAT and OCCUPIED_SEAT not in adjacents:
                new_state = OCCUPIED_SEAT
                state_changed = True
            elif (
                col == OCCUPIED_SEAT
                and adjacents.count(OCCUPIED_SEAT) >= num_occupied_to_be_empty
            ):
                new_state = EMPTY_SEAT
                state_changed = True
            new_map[x].append(new_state)
    return new_map, state_changed


def count_occupied(map):
    count = 0
    for x in map:
        count += x.count(OCCUPIED_SEAT)
    return count


state_changed = True
last_map = map
while state_changed:
    new_map, state_changed = calc_new_map(last_map)
    last_map = new_map

print(count_occupied(new_map))

# Part 2
# (x, y) -> [(seat_x_1, seat_y_1), (seat_x_2, seat_y_2), ...]
line_of_sight_cache = {}


def trace_cordinate_on_line(slope_x, slope_y, x, y, max_x, max_y):
    if slope_x == 0 and slope_y == 0:
        raise ValueError("Line to nowhere")
    while True:
        if slope_x < 0 and x == 0:
            return
        elif slope_x > 0 and x == max_x:
            return
        if slope_y < 0 and y == 0:
            return
        elif slope_y > 0 and y == max_y:
            return
        # Generate new coordinate
        x += slope_x
        y += slope_y
        yield x, y


def chair_at_coordinate(old_map, x, y):
    # print(f"Checking {x}, {y}")
    # print(f"Bounds {len(old_map) - 1}, {len(old_map[0]) - 1}")
    return old_map[x][y] in [OCCUPIED_SEAT, EMPTY_SEAT]


def get_adjacents_by_line_of_sight(old_map, x, y):
    if (x, y) in line_of_sight_cache:
        return [old_map[a][b] for a, b in line_of_sight_cache[(x, y)]]
    to_be_cached = []
    max_x = len(old_map) - 1
    max_y = len(old_map[0]) - 1
    lines = [
        (-1, -1),
        (0, -1),
        (1, -1),  # up_left, up, up right
        (-1, 0),
        (1, 0),  # left, right
        (-1, 1),
        (0, 1),
        (1, 1),
    ]  # down_left, down, down right
    for slope_x, slope_y in lines:
        for pos_x, pos_y in trace_cordinate_on_line(
            slope_x, slope_y, x, y, max_x, max_y
        ):
            if chair_at_coordinate(old_map, pos_x, pos_y):
                to_be_cached.append((pos_x, pos_y))
                break
    line_of_sight_cache[(x, y)] = to_be_cached
    return [old_map[a][b] for a, b in to_be_cached]


state_changed = True
last_map = map
while state_changed:
    new_map, state_changed = calc_new_map(
        last_map,
        adjacent_method=get_adjacents_by_line_of_sight,
        num_occupied_to_be_empty=5,
    )
    last_map = new_map

print(count_occupied(new_map))
