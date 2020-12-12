from enum import Enum

FLOOR = "."
EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"


class ChairMethod(Enum):
    ADJACENT = 0
    SIGHT = 1


class CoordinateCache:
    def __init__(self):
        self._cache = {}

    def check_in_cache(self, x, y):
        return (x, y) in self._cache

    def get_cache_value(self, x, y):
        if not self.check_in_cache(x, y):
            return None
        return self._cache[(x, y)]

    def cache(self, x, y, values):
        self._cache[(x, y)] = values


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


class SeatMap:
    def __init__(self, other_map=None):
        self.inner = []
        if other_map is not None:
            self.inner = [[] for _ in other_map.inner]

    def add_row(self):
        self.inner.append([])

    @property
    def row_length(self):
        return len(self.inner)

    @property
    def col_length(self):
        if self.row_length == 0:
            return 0
        return len(self.inner[0])

    def add_column_value(self, row, value):
        self.inner[row].append(value)

    def chair_at_coordinate(self, x, y):
        return self.inner[x][y] in [OCCUPIED_SEAT, EMPTY_SEAT]

    @property
    def num_occupied(self):
        count = 0
        for x in self.inner:
            count += x.count(OCCUPIED_SEAT)
        return count

    def get_adjacents(self, x, y, cache):
        v = cache.get_cache_value(x, y)
        if v is not None:
            return [self.inner[a][b] for a, b in v]
        to_be_cached = []
        top_edge = x == 0
        bottom_edge = x + 1 == self.row_length
        left_edge = y == 0
        right_edge = y + 1 == self.col_length

        if not top_edge:
            # Diagonal Up Left
            if not left_edge:
                to_be_cached.append((x - 1, y - 1))
            # Up
            to_be_cached.append((x - 1, y))
            # Diagonal Up Right
            if not right_edge:
                to_be_cached.append((x - 1, y + 1))
        if not left_edge:
            # Left
            to_be_cached.append((x, y - 1))
        if not right_edge:
            # Right
            to_be_cached.append((x, y + 1))
        if not bottom_edge:
            # Diagonal bottom left
            if not left_edge:
                to_be_cached.append((x + 1, y - 1))
            # Down
            to_be_cached.append((x + 1, y))
            # Bottom right
            if not right_edge:
                to_be_cached.append((x + 1, y + 1))
        cache.cache(x, y, to_be_cached)
        return [self.inner[a][b] for a, b in to_be_cached]

    def get_adjacents_by_line_of_sight(self, x, y, cache):
        v = cache.get_cache_value(x, y)
        if v is not None:
            return [self.inner[a][b] for a, b in v]
        to_be_cached = []
        max_x = self.row_length - 1
        max_y = self.col_length - 1
        lines = [
            (-1, -1),  # up_left
            (0, -1),  # up
            (1, -1),  # up_right
            (-1, 0),  # left
            (1, 0),  # right
            (-1, 1),  # down left
            (0, 1),  # down
            (1, 1),  # right
        ]
        for slope_x, slope_y in lines:
            for pos_x, pos_y in trace_cordinate_on_line(
                slope_x, slope_y, x, y, max_x, max_y
            ):
                if self.chair_at_coordinate(pos_x, pos_y):
                    to_be_cached.append((pos_x, pos_y))
                    break
        cache.cache(x, y, to_be_cached)
        return [self.inner[a][b] for a, b in to_be_cached]

    def calc_new_map(self, chair_method, num_occupied_to_be_empty, cache):
        adjacent_method = None
        if chair_method == ChairMethod.ADJACENT:
            adjacent_method = self.get_adjacents
        if chair_method == ChairMethod.SIGHT:
            adjacent_method = self.get_adjacents_by_line_of_sight
        new_map = SeatMap(self)
        state_changed = False
        for x, row in enumerate(self.inner):
            for y, col in enumerate(row):
                new_state = col
                if col == FLOOR:
                    new_map.add_column_value(x, new_state)
                    continue
                adjacents = adjacent_method(x, y, cache)
                if col == EMPTY_SEAT and OCCUPIED_SEAT not in adjacents:
                    new_state = OCCUPIED_SEAT
                    state_changed = True
                elif (
                    col == OCCUPIED_SEAT
                    and adjacents.count(OCCUPIED_SEAT) >= num_occupied_to_be_empty
                ):
                    new_state = EMPTY_SEAT
                    state_changed = True
                new_map.add_column_value(x, new_state)
        return new_map, state_changed


def read_map(filename="input"):
    input_map = SeatMap()
    with open(filename, "r") as f:
        for i, x in enumerate(f):
            if x == "\n":
                continue
            input_map.add_row()
            for y in x.strip():
                input_map.add_column_value(i, y)
    return input_map


def part1(start_map):
    state_changed = True
    cache = CoordinateCache()
    last_map = start_map
    while state_changed:
        new_map, state_changed = last_map.calc_new_map(ChairMethod.ADJACENT, 4, cache)
        last_map = new_map

    print(new_map.num_occupied)


def part2(start_map):
    state_changed = True
    last_map = start_map
    cache = CoordinateCache()
    while state_changed:
        new_map, state_changed = last_map.calc_new_map(ChairMethod.SIGHT, 5, cache)
        last_map = new_map

    print(new_map.num_occupied)


input_map = read_map()
part1(input_map)
part2(input_map)
