class Customs:
    def __init__(self):
        self.set = set()
        self.part2Set = set()
        self.first = True

    def parse_string(self, str):
        self.set = self.set.union(set(str.strip()))
        if self.first:
            self.part2Set = self.part2Set.union(set(str.strip()))
            self.first = False
        else:
            self.part2Set = self.part2Set.intersection(set(str.strip()))

    def count(self):
        return len(self.set)

    def count2(self):
        return len(self.part2Set)


def parse_input():
    with open("input", "r") as f:
        c = Customs()
        for x in f:
            if x == "\n":
                yield c
                c = Customs()
            else:
                c.parse_string(x)
        yield c


inputs = [x for x in parse_input()]
print("Part1: ", sum(x.count() for x in inputs))
print("Part2: ", sum(x.count2() for x in inputs))
