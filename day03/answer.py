import math


class Toboggan:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, right, down, max_right, max_down):
        if max_down == self.y:
            return
        self.x = (self.x + right) % max_right
        self.y = self.y + down


class SkiMap:
    def __init__(self, strings):
        self._map = [x.strip("\n") for x in strings]
        self.tree = "#"
        self.maxY = len(self._map) - 1
        self.maxX = len(self._map[0])

    def is_on_map(self, character):
        return character.x <= self.maxX and character.y <= self.maxY

    def is_on_tree(self, character):
        if not self.is_on_map(character):
            raise ValueError("Flew off the map")
        return self._map[character.y][character.x] == self.tree


class Slope:
    def __init__(self, right, down):
        self.right = right
        self.down = down

    def move(self, character, map):
        character.move(self.right, self.down, map.maxX, map.maxY)

    def __str__(self):
        return f"Right {self.right} Down {self.down}"


skimap = None
with open("input", "r") as f:
    skimap = SkiMap([r for r in f])

possible_slopes = [Slope(1, 1), Slope(3, 1), Slope(5, 1), Slope(7, 1), Slope(1, 2)]

results = []

for slope in possible_slopes:
    me = Toboggan()
    # Check starting position for a collision
    trees_hit = 1 if skimap.is_on_tree(me) else 0

    while me.y < skimap.maxY:
        slope.move(me, skimap)
        if skimap.is_on_tree(me):
            trees_hit += 1

    print(slope, "Trees hit: ", trees_hit)
    results.append(trees_hit)

print("final result: ", math.prod(results))
