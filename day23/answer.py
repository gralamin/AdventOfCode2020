import time
from collections import deque
import copy


class Cup:
    def __init__(self, label):
        self.label = int(label)

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return self.label == other.label

    def get_debug(self, cur_cup_is):
        if cur_cup_is == self:
            return f"({self.label})"
        return f"{self.label}"

    def __repr__(self):
        return f"Cup({self.label})"

    @property
    def value(self):
        # I used these interchangably, just add a property instead
        # of fixing me
        return self.label


class CupGame:
    def __init__(self, cups):
        self.cups = deque(cups)
        self.move = 1
        self.cur_cup = self.cups[0]
        self.cur_cup_index = 0
        self.highest_cup_value = max([c.value for c in self.cups])
        self.lowest_cup_value = min([c.value for c in self.cups])

    def play_round(self, debug):
        if debug:
            print(f"-- move {self.move} --")
            self._print_cups()

        removed_cups = self._remove_cups(3, debug)
        destination_cup = self._get_destination_cup(removed_cups, debug)

        self._reinsert_cups(destination_cup, removed_cups)
        self._select_new_cup()
        self.move += 1
        if debug:
            print("")

    def _print_cups(self):
        cup_str = " ".join([cup.get_debug(self.cur_cup) for cup in self.cups])
        print(f"cups: {cup_str}")

    def _remove_cups(self, num, debug):
        # Imagine 1 (4) 2 3, and grab 3.
        # cur_cup_index = 1, 1 + 3 = 4
        # so need to grab 2, 3 (2, 3) in index
        # and 1 (0). We can use modulous to do this
        last_cup_index = self.cur_cup_index + num
        left_overs = (
            last_cup_index % (len(self.cups) - 1)
            if last_cup_index > len(self.cups) - 1
            else 0
        )
        last_cup_index = min(last_cup_index, len(self.cups) - 1)
        indexes_to_remove = []
        for i in range(self.cur_cup_index + 1, last_cup_index + 1):
            indexes_to_remove.append(i)
        for i in range(left_overs):
            indexes_to_remove.append(i)
        values_to_remove = [self.cups[i] for i in indexes_to_remove]
        for v in values_to_remove:
            self.cups.remove(v)
        if debug:
            cup_str = ", ".join(
                [cup.get_debug(self.cur_cup) for cup in values_to_remove]
            )
            print(f"pick up: {cup_str}")
        return values_to_remove

    def _get_destination_cup(self, removed_cups, debug):
        removed_cups_labels = [c.label for c in removed_cups]

        destination_value = int(self.cur_cup.label) - 1
        if destination_value < self.lowest_cup_value:
            destination_value = self.highest_cup_value
        while destination_value in removed_cups_labels:
            destination_value -= 1
            if destination_value < self.lowest_cup_value:
                destination_value = self.highest_cup_value

        if debug:
            print(f"destination: {destination_value}")
        for cup in self.cups:
            if cup.label == destination_value:
                return cup

    def _reinsert_cups(self, destination_cup, removed_cups):
        destination_cup_index = 0
        for index, cup in enumerate(self.cups):
            if destination_cup == cup:
                destination_cup_index = index

        for index, cup in enumerate(removed_cups):
            insert_index = destination_cup_index + index + 1
            self.cups.insert(insert_index, cup)

    def _select_new_cup(self):
        # Cur cup could have mvoed, find its index again
        for index, cup in enumerate(self.cups):
            if cup == self.cur_cup:
                self.cur_cup_index = index
                break
        self.cur_cup_index += 1
        self.cur_cup_index = self.cur_cup_index % len(self.cups)
        self.cur_cup = self.cups[self.cur_cup_index]

    def get_ordering(self, debug):
        if debug:
            print("-- final --")
            self._print_cups()
        found_one = False
        before_one = []
        after_one = []
        for x in self.cups:
            if x.label == 1:
                found_one = True
                continue
            if not found_one:
                before_one.append(x)
            else:
                after_one.append(x)
        ordering = after_one + before_one
        return "".join([str(x.label) for x in ordering])


def part1(cups, debug=False, moves=100):
    engine = CupGame(cups)
    for _ in range(moves):
        engine.play_round(debug)
    return engine.get_ordering(debug)


def get_input():
    with open("input", "r") as f:
        for x in f:
            a = x.strip()
            if not a:
                continue
            for z in a:
                yield Cup(z)


if __name__ == "__main__":
    cups = list(get_input())
    p1cups = copy.deepcopy(cups)

    start = time.perf_counter()
    print("Part1:", part1(p1cups))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
