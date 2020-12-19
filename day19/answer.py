import re
import time

single_character_rule = re.compile('"(.)"')


class BinaryTreeNode:
    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.chil2


class Rule:
    def __init__(self, in_str):
        number, criteria = in_str.split(":")
        self.number = int(number)
        self.character = None
        self.rule_conditions = []

        criteria = criteria.strip()
        match = single_character_rule.match(criteria)
        if match:
            self.character = match.groups()[0]
        else:
            for x in criteria.split("|"):
                self.rule_conditions.append([int(x) for x in x.strip().split(" ")])

    def __eq__(self, other):
        return self.number == other.number

    def __lt__(self, other):
        return self.number < other.number

    def __gt__(self, other):
        return self.number > other.number

    def __hash__(self):
        return hash(self.number)

    def into_regex(self, all_rules, cache):
        if self.number in cache:
            return cache[self.number]

        if self.character:
            cache[self.number] = self.character
            return self.character
        else:
            regexes = []
            for possible_combos in self.rule_conditions:
                cur_regex = ""
                for x in possible_combos:
                    cur_regex = cur_regex + all_rules[x].into_regex(all_rules, cache)
                regexes.append(cur_regex)
            regex = "(" + "|".join(regexes) + ")"
            cache[self.number] = regex
            return regex


def match(message, all_rules):
    results = _match(0, 0, message, all_rules)
    return any([result == len(message) for result in results])


def _match(rule_index, message_index, message, all_rules):
    if message_index == len(message):
        return []
    results = []
    new_rule = all_rules[rule_index]
    if new_rule.character:
        if new_rule.character == message[message_index]:
            # return the length matched
            return [message_index + 1]
        else:
            return []
    for possibe_combination in new_rule.rule_conditions:
        start_index = [message_index]
        for sub_rule in possibe_combination:
            new_start_index = []
            for i in start_index:
                sub_results = _match(sub_rule, i, message, all_rules)
                new_start_index.extend(sub_results)
            start_index = new_start_index
        results.extend(start_index)
    return results


def get_input():
    section = 0
    rules = []
    messages = []
    with open("input", "r") as f:
        for x in f:
            if x == "\n" and section == 0:
                section += 1
                continue
            x = x.strip()
            if section == 0:
                rules.append(Rule(x))
            elif section == 1:
                if not x:
                    continue
                messages.append(x)
    return rules, messages


def part1(rules, messages):
    # Regexes sufficient here, don't need a full abstract syntax tree.
    rule_dict = {rule.number: rule for rule in rules}
    matches = []
    rule_cache = {}
    regex = rule_dict[0].into_regex(rule_dict, rule_cache)
    for message in messages:
        if re.match("^" + regex + "$", message):
            matches.append(message)
    return len(matches)


def part2(rules, messages):
    rule_dict = {rule.number: rule for rule in rules}
    rule_dict[8] = Rule("8: 42 | 42 8")
    rule_dict[11] = Rule("11: 42 31 | 42 11 31")
    matches = [match(x, rule_dict) for x in messages]
    matches = [x for x in matches if x]
    return len(matches)


if __name__ == "__main__":
    rules, messages = get_input()
    start = time.perf_counter()
    print("Part1:", part1(rules, messages))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
    start = time.perf_counter()
    print("Part 2:", part2(rules, messages))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
