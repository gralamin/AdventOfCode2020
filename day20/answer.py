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
                left_fit = grid[row][col - 1].matches_left_border(version)
            if row > 0:
                top_fit = grid[row - 1][col].matches_top_border(version)
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


def part1(all_tiles):
    # Precompute possible tiles
    tile_candidates_by_number = {}
    for tile in all_tiles:
        # I have aphantsia, so I can't visualize how a tile looks after each of these.
        # I would have to manually draw it out and do each one.
        # I suspect therefore, I have duplicates in here.
        tile_candidates_by_number[tile.number] = [
            tile,
            tile.rotate(),
            tile.rotate().rotate(),
            tile.rotate().rotate().rotate(),
            tile.flip(),
            tile.rotate().flip(),
            tile.rotate().rotate().flip(),
            tile.rotate().rotate().rotate().flip(),
        ]
    grid_size = int(math.sqrt(len(all_tiles)))
    grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    result, filled_grid = backtrack_tiles(tile_candidates_by_number, set(), grid, 0, 0)
    if not result:
        raise ValueError("Failed to find solution")

    top_left = filled_grid[0][0].number
    top_right = filled_grid[0][grid_size - 1].number
    bottom_left = filled_grid[grid_size - 1][0].number
    bottom_right = filled_grid[grid_size - 1][grid_size - 1].number
    return top_left * top_right * bottom_left * bottom_right


if __name__ == "__main__":
    tiles = get_input()
    start = time.perf_counter()
    print("Part1:", part1(tiles))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
