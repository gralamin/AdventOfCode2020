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


def calc_new_map(old_map):
    new_map = [[] for _ in old_map]
    state_changed = False
    for x, row in enumerate(old_map):
        for y, col in enumerate(row):
            new_state = col
            if col == FLOOR:
                new_map[x].append(new_state)
                continue
            adjacents = get_adjacents(old_map, x, y)
            if col == EMPTY_SEAT and OCCUPIED_SEAT not in adjacents:
                new_state = OCCUPIED_SEAT
                state_changed = True
            elif col == OCCUPIED_SEAT and adjacents.count(OCCUPIED_SEAT) >= 4:
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
