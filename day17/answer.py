from enum import Enum
import time

ACTIVE = "#"
INACTIVE = "."


class CubeState(Enum):
    ACTIVE = True
    INACTIVE = False


class Coordinate3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def is_neighbor(self, other):
        if self == other:
            return False
        diff_x = abs(self.x - other.x)
        diff_y = abs(self.y - other.y)
        diff_z = abs(self.z - other.z)
        return diff_x <= 1 and diff_y <= 1 and diff_z <= 1

    def generate_neighbors(self):
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if not (x == 0 and y == 0 and z == 0):
                        yield type(self)(self.x + x, self.y + y, self.z + z)


class Coordinate4D(Coordinate3D):
    def __init__(self, x, y, z, w):
        super().__init__(x, y, z)
        self.w = w

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.w})"

    def __eq__(self, other):
        return (
            self.x == other.x
            and self.y == other.y
            and self.z == other.z
            and self.w == other.w
        )

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.w))

    def is_neighbor(self, other):
        if self == other:
            return False
        super_answer = super().is_neighbor(other)
        diff_w = abs(self.w - other.w)
        return super_answer and diff_w <= 1

    def generate_neighbors(self):
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    for w in range(-1, 2):
                        if not (x == 0 and y == 0 and z == 0 and w == 0):
                            yield type(self)(
                                self.x + x, self.y + y, self.z + z, self.w + w
                            )


class ConwayCube:
    def __init__(self, coordinate, state):
        self.coordinate = coordinate
        self.state = state

    def transition(self, neighbors, active_range, inactive_value):
        if self.active and len(neighbors) in active_range:
            return ConwayCube(self.coordinate, CubeState.ACTIVE)
        elif self.active:
            return ConwayCube(self.coordinate, CubeState.INACTIVE)
        elif not self.active and len(neighbors) == inactive_value:
            return ConwayCube(self.coordinate, CubeState.ACTIVE)
        else:
            return ConwayCube(self.coordinate, CubeState.INACTIVE)

    def is_neighbor(self, other):
        return self.coordinate.is_neighbor(other.coordinate)

    def generate_neighbor_coordinates(self):
        return self.coordinate.generate_neighbors()

    def is_at(self, coordinate):
        return self.coordinate == coordinate

    @property
    def active(self):
        return self.state == CubeState.ACTIVE

    def __hash__(self):
        return hash((self.coordinate, self.state))

    def __eq__(self, other):
        return self.coordinate == other.coordinate and self.state == other.state

    def __repr__(self):
        return f"Cube({self.coordinate}, {self.state})"


class CubeGrid3D:
    def __init__(self, cubes):
        self.active_cubes = set([c for c in cubes if c.active])
        self.inactive_cubes = set()
        self.populate_inactive()

    def populate_inactive(self):
        # We only need to track those with at least 1 active neighbor
        active_coordinates = list(self.get_active_coordinates())
        for active_cube in self.active_cubes:
            for coordinate in active_cube.generate_neighbor_coordinates():
                if coordinate in active_coordinates:
                    continue
                new_cube = ConwayCube(coordinate, CubeState.INACTIVE)
                self.inactive_cubes.add(new_cube)

    def get_active_coordinates(self):
        for cube in self.active_cubes:
            yield cube.coordinate

    @property
    def num_active(self):
        return len(self.active_cubes)

    def cycle(self, active_range=None, inactive_value=3):
        active_range = [2, 3] if active_range is None else active_range
        cycled_cubes = []
        for cube in self.active_cubes:
            # don't need to get inactive neighbors
            active_neighbors = [c for c in self.active_cubes if cube.is_neighbor(c)]
            cycled_cubes.append(
                cube.transition(active_neighbors, active_range, inactive_value)
            )
        for cube in self.inactive_cubes:
            # don't need to get inactive neighbors
            active_neighbors = [c for c in self.active_cubes if cube.is_neighbor(c)]
            cycled_cubes.append(
                cube.transition(active_neighbors, active_range, inactive_value)
            )
        return type(self)(cycled_cubes)

    def __repr__(self):
        result = []
        min_x = float("inf")
        min_y = float("inf")
        min_z = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")
        max_z = float("-inf")
        active_coordinates = []
        for coordinate in self.get_active_coordinates():
            min_x = min(min_x, coordinate.x)
            min_y = min(min_y, coordinate.y)
            min_z = min(min_z, coordinate.z)
            max_x = max(max_x, coordinate.x)
            max_y = max(max_y, coordinate.y)
            max_z = max(max_z, coordinate.z)
            active_coordinates.append(coordinate)
        if min_x == float("inf"):
            min_x = 0
            max_x = 0
        if min_y == float("inf"):
            min_y = 0
            max_y = 0
        if min_z == float("inf"):
            min_z = 0
            max_z = 0

        for z in range(min_z, max_z + 1):
            new_z_layer = [f"z={z}"]
            z_grid = []
            for y in range(min_y, max_y + 1):
                row_in_progress = []
                for x in range(min_x, max_x + 1):
                    character = (
                        ACTIVE
                        if Coordinate3D(x, y, z) in active_coordinates
                        else INACTIVE
                    )
                    row_in_progress.append(character)
                z_grid.append("".join(row_in_progress))
            new_z_layer.append("\n".join(z_grid))
            result.append("")
            result.append("\n".join(new_z_layer))
        return "\n".join(result)


class CubeGrid4D(CubeGrid3D):
    def __repr__(self):
        result = []
        min_x = float("inf")
        min_y = float("inf")
        min_z = float("inf")
        min_w = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")
        max_z = float("-inf")
        max_w = float("-inf")
        active_coordinates = []
        for coordinate in self.get_active_coordinates():
            min_x = min(min_x, coordinate.x)
            min_y = min(min_y, coordinate.y)
            min_z = min(min_z, coordinate.z)
            min_w = min(min_w, coordinate.w)
            max_x = max(max_x, coordinate.x)
            max_y = max(max_y, coordinate.y)
            max_z = max(max_z, coordinate.z)
            max_w = max(max_w, coordinate.w)
            active_coordinates.append(coordinate)
        if min_x == float("inf"):
            min_x = 0
            max_x = 0
        if min_y == float("inf"):
            min_y = 0
            max_y = 0
        if min_z == float("inf"):
            min_z = 0
            max_z = 0
        if min_w == float("inf"):
            min_w = 0
            max_w = 0

        for w in range(min_w, min_w + 1):
            for z in range(min_z, max_z + 1):
                new_z_layer = [f"z={z}, w={w}"]
                z_grid = []
                for y in range(min_y, max_y + 1):
                    row_in_progress = []
                    for x in range(min_x, max_x + 1):
                        character = (
                            ACTIVE
                            if Coordinate4D(x, y, z, w) in active_coordinates
                            else INACTIVE
                        )
                        row_in_progress.append(character)
                    z_grid.append("".join(row_in_progress))
                new_z_layer.append("\n".join(z_grid))
                result.append("")
                result.append("\n".join(new_z_layer))
        return "\n".join(result)


def get_input():
    with open("input", "r") as f:
        lines = [line.strip() for line in f]
        lines = [line for line in lines if line != ""]
        z = 0
        # y is each line
        # x is each entry
        cubes = []
        for y, line in enumerate(lines):
            for x, character in enumerate(line):
                if character == ACTIVE:
                    cubes.append(ConwayCube(Coordinate3D(x, y, z), CubeState.ACTIVE))
        return cubes


def part_1(input_state, num_cycles=6, debug=False):
    input_state = CubeGrid3D(input_state)
    cur_state = input_state
    for i in range(num_cycles):
        if debug:
            print(f"\nCycle {i}")
            print(cur_state)
        cur_state = cur_state.cycle()
    if debug:
        print(f"\nCycle {num_cycles}")
        print(cur_state)
    return cur_state.num_active


def part_2(input_state, num_cycles=6, debug=False):
    input_state = [
        ConwayCube(
            Coordinate4D(c.coordinate.x, c.coordinate.y, c.coordinate.z, 0), c.state
        )
        for c in input_state
    ]
    input_state = CubeGrid4D(input_state)
    cur_state = input_state
    for i in range(num_cycles):
        if debug:
            print(f"\nCycle {i}")
            print(cur_state)
        cur_state = cur_state.cycle()
    if debug:
        print(f"\nCycle {num_cycles}")
        print(cur_state)
    return cur_state.num_active


if __name__ == "__main__":
    input_state = get_input()
    start = time.perf_counter()
    print("Part 1:", part_1(input_state))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
    start = time.perf_counter()
    print("Part 2:", part_2(input_state))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
