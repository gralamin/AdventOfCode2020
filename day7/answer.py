import re

descriptor_map = {}
shiny_gold_cache = {}
sub_bag_cache = {}


class BagMap:
    # A Bag here is basically a tree, with:
    # Descriptors for it (a key for the descriptor_map)
    # sub nodes containing a link to a bag, and an associated number.
    def __init__(self, descriptors):
        self.descriptors = descriptors
        self.subnodes = {}

    def add_subnode(self, number, descriptors):
        # print(f"Adding {descriptors} to {self.descriptors}")
        subBag = descriptor_map.setdefault(descriptors, BagMap(descriptors))
        # If the same subbag shows up for some reason, just add to the total number.
        self.subnodes[subBag] = self.subnodes.get(subBag, 0) + number

    def __hash__(self):
        return hash(self.descriptors)

    def __eq__(self, other):
        return self.descriptors == other.descriptors

    def __ne__(self, other):
        return self.descriptors != other.descriptors

    # Essentially a depth first search, with optimizations to not repeat
    # known results.
    def contains_shiny_gold(self):
        if self in shiny_gold_cache:
            return shiny_gold_cache[self]
        result = any(x.descriptors == "shiny gold" for x in self.subnodes) or any(
            x.contains_shiny_gold() for x in self.subnodes
        )
        shiny_gold_cache[self] = result
        return result

    def sub_bag_count(self):
        if self in sub_bag_cache:
            return sub_bag_cache[self]
        total = 0
        for sub_bag, multiplier in self.subnodes.items():
            # Non-leaf node, multiple its sub by the the count. On a leaf node,
            # becomes 0
            inside_bag_count = sub_bag.sub_bag_count() * multiplier
            total += multiplier
            total += inside_bag_count
        sub_bag_cache[self] = total
        return total


# with open("input_test", "r") as f:
with open("input", "r") as f:
    for x in f:
        x = x.strip()
        bags_split = x.split("bags contain")
        descriptors = bags_split[0].strip()
        # print(f"parsing {descriptors}")
        bag = descriptor_map.setdefault(descriptors, BagMap(descriptors))
        for sub_bag_input in bags_split[1].split(","):
            # print(f"searching '{sub_bag_input}'")
            regex_match = re.search("(\\d+) (.*) bag", sub_bag_input)
            if not regex_match:
                continue
            groups = regex_match.groups()
            num = int(groups[0])
            sub_descriptors = groups[1]
            bag.add_subnode(num, sub_descriptors)

results = [x for x in descriptor_map.values() if x.contains_shiny_gold()]
print(len(results), "Contain shiny gold bags")

print(f"Shiny gold contains {descriptor_map['shiny gold'].sub_bag_count()} other bags.")
