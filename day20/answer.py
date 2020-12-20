import math
import time


class Tile:
    def __init__(self, number, tile_img):
        self.number = number
        self.tile = tile_img

    def rotate(self):
        new_tile = [[None for _ in self.tile] for _ in self.tile]
        for row in range(len(self.tile)):
            for col in range(len(self.tile)):
                new_row = col
                new_col = len(self.tile) - 1 - row
                new_tile[new_row][new_col] = self.tile[row][col]

        return Tile(self.number, new_tile)

    def flip(self):
        new_tile = [[None for _ in self.tile] for _ in self.tile]
        for row in range(len(self.tile)):
            for col in range(len(self.tile)):
                new_row = row
                new_col = len(self.tile) - 1 - col
                new_tile[new_row][new_col] = self.tile[row][col]
        return Tile(self.number, new_tile)

    def __eq__(self, other):
        return self.number == other.number

    def matches_left_border(self, other):
        if other is None:
            raise ValueError("Comparing vs nothing")
        # Left border of self, = everything at 0 per row
        # Right border of other, = everything at -1 per row
        left_border = [x[0] for x in self.tile]
        right_border = [x[-1] for x in other.tile]
        return all(x == y for x, y in zip(left_border, right_border))

    def matches_right_border(self, other):
        return other.matches_left_border(self)

    def matches_top_border(self, other):
        # top border of self, = everything at 0
        # bottom border of other, = everything at -1
        top_border = self.tile[0]
        bottom_border = other.tile[-1]
        return all(x == y for x, y in zip(top_border, bottom_border))

    def matches_bottom_border(self, other):
        return other.matches_top_border(self)

    def __repr__(self):
        return f"Tile({self.number})"

    def trim_borders(self):
        new_tile = [
            [None for _ in range(len(self.tile) - 2)] for _ in range(len(self.tile) - 2)
        ]
        for row in range(len(self.tile)):
            if row == 0 or row == len(self.tile) - 1:
                continue
            for col in range(len(self.tile)):
                if col == 0 or col == len(self.tile) - 1:
                    continue
                new_row = row - 1
                new_col = col - 1
                new_tile[new_row][new_col] = self.tile[row][col]
        new_tile = Tile(self.number, new_tile)
        return new_tile

    def pretty(self):
        results = [f"Tile {self.number}:"]
        x = ["".join(z) for z in self.tile]
        results.extend(x)
        return "\n".join(results)


class Image:
    def __init__(self, trimmed_grid):
        grid_multplier = len(trimmed_grid)
        one_tile = trimmed_grid[0][0]
        image = [
            [None for _ in range(len(one_tile) * grid_multplier)]
            for _ in range(len(one_tile) * grid_multplier)
        ]
        for tile_y, tile_row in enumerate(trimmed_grid):
            for tile_x, tile in enumerate(tile_row):
                for y, row in enumerate(tile):
                    for x, v in enumerate(row):
                        dest_y = tile_y * len(one_tile) + y - 1
                        dest_x = tile_x * len(one_tile) + x - 1
                        image[dest_y][dest_x] = v
        self.tile = Tile(0, image)

    @property
    def roughness(self):
        v = 0
        for y in self.tile.tile:
            for x in y:
                if x == "#":
                    v += 1
        return v

    def find_sea_monsters(self):
        # sea monster as relative coordinates
        # This is (y, x)
        sea_monster = [
            (0, 18),
            (1, 0),
            (1, 5),
            (1, 6),
            (1, 11),
            (1, 12),
            (1, 17),
            (1, 18),
            (1, 19),
            (2, 1),
            (2, 4),
            (2, 7),
            (2, 10),
            (2, 13),
            (2, 16),
        ]

        monster_count = 0
        possible_tiles = [
            self.tile,
            self.tile.flip(),
            self.tile.rotate(),
            self.tile.rotate().flip(),
            self.tile.rotate().rotate(),
            self.tile.rotate().rotate().flip(),
            self.tile.rotate().rotate().rotate(),
            self.tile.rotate().rotate().rotate().flip(),
        ]
        for tile in possible_tiles:
            monster_count, marked_tile = self._mark_sea_monster(tile, sea_monster)
            if not monster_count:
                continue
            self.tile = marked_tile
            # print(self.tile.pretty())
            return True
        return False

    def _mark_sea_monster(self, tile, sea_monster):
        """Mark all sea monster coordinates with O"""
        monster_count = 0
        for y, row in enumerate(tile.tile):
            for x, v in enumerate(row):
                found = True
                for coords in sea_monster:
                    offset_y = y + coords[0]
                    offset_x = x + coords[1]
                    if offset_x >= len(tile.tile) or offset_y >= len(tile.tile):
                        found = False
                        break
                    if tile.tile[offset_y][offset_x] != "#":
                        found = False
                        break
                if found:
                    monster_count += 1
                    for coords in sea_monster:
                        offset_y = y + coords[0]
                        offset_x = x + coords[1]
                        tile.tile[offset_y][offset_x] = "O"
        return monster_count, tile


def read_tile_from_strings(strings):
    number = strings[0]
    tile_number = int(number.split(" ")[1][:-1])
    tile_img = []
    for x in strings[1:]:
        tile_img.append([z for z in x.strip()])
    return Tile(tile_number, tile_img)


def get_input():
    tiles = []
    with open("input", "r") as f:
        possible_tile = []
        for x in f:
            x = x.strip()
            if x == "":
                tiles.append(read_tile_from_strings(possible_tile))
                possible_tile = []
            else:
                possible_tile.append(x)
        if possible_tile:
            tiles.append(read_tile_from_strings(possible_tile))
    return tiles


def backtrack_tiles(tiles, tiles_in_use, grid, row, col):
    # print(f"Checking {row} {col} (grid length is: {len(grid)})")
    if row >= len(grid) or col >= len(grid):
        return True, grid

    for tile_number in tiles:
        if tile_number in tiles_in_use:
            continue

        tiles_in_use.add(tile_number)
        # Check each version of the tile:
        for version in tiles[tile_number]:
            left_fit, top_fit = True, True
            if col > 0:
                left_fit = version.matches_left_border(grid[row][col - 1])
            if row > 0:
                top_fit = version.matches_top_border(grid[row - 1][col])
            if left_fit and top_fit:
                # So this looks like its matching
                grid[row][col] = version
                next_col = (col + 1) % len(grid)
                next_row = row + 1 if next_col == 0 else row
                backtrack_result, new_grid = backtrack_tiles(
                    tiles, tiles_in_use, grid, next_row, next_col
                )
                if backtrack_result:
                    # print(f"found solution {new_grid}")
                    return True, new_grid
        # Could not find a version, backtrack
        grid[row][col] = None
        tiles_in_use.remove(tile_number)
    # No candidates, fail
    return False, grid


def find_grid(all_tiles):
    # Precompute possible tiles
    tile_candidates_by_number = {}
    for tile in all_tiles:
        # I have aphantsia, so I can't visualize how a tile looks after each of these.
        # I would have to manually draw it out and do each one.
        # I suspect therefore, I have duplicates in here.
        tile_candidates_by_number[tile.number] = [
            tile,
            tile.rotate().rotate().flip(),
            tile.flip(),
            tile.rotate(),
            tile.rotate().rotate(),
            tile.rotate().rotate().rotate(),
            tile.rotate().rotate().rotate().flip(),
            tile.rotate().flip(),
        ]
    grid_size = int(math.sqrt(len(all_tiles)))
    grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    result, filled_grid = backtrack_tiles(tile_candidates_by_number, set(), grid, 0, 0)

    if not result:
        raise ValueError("Failed to find solution")
    return filled_grid


def part1(all_tiles):
    filled_grid = find_grid(all_tiles)
    grid_size = int(math.sqrt(len(all_tiles)))
    top_left = filled_grid[0][0].number
    top_right = filled_grid[0][grid_size - 1].number
    bottom_left = filled_grid[grid_size - 1][0].number
    bottom_right = filled_grid[grid_size - 1][grid_size - 1].number
    return top_left * top_right * bottom_left * bottom_right


def part2(all_tiles):
    filled_grid = find_grid(all_tiles)
    trimmed_grid = []
    for y, row in enumerate(filled_grid):
        trimmed_grid.append([])
        for tile in row:
            trimmed = tile.trim_borders()
            trimmed_grid[y].append(trimmed.tile)

    image = Image(trimmed_grid)
    result = image.find_sea_monsters()
    if not result:
        raise ValueError("Sea monsters not found")
    return image.roughness


if __name__ == "__main__":
    tiles = get_input()
    start = time.perf_counter()
    print("Part1:", part1(tiles))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
    print("Part2:", part2(tiles))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
