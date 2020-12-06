class Customs:
    def __init__(self):
        self.set = set()

    def parse_string(self, str):
        self.set = self.set.union(set(str.strip()))

    def count(self):
        return len(self.set)


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


print(sum(x.count() for x in parse_input()))
