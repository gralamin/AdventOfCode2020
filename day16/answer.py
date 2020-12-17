import re
import math

RULE_REGEX = re.compile("([a-zA-Z ]+): (\\d+)-(\\d+) or (\\d+)-(\\d+)")
DEPART = "departure"


class Rule:
    def __init__(self, name, valid_range):
        self.name = name
        self.valid_range = valid_range

    def is_valid(self, value):
        return value in self.valid_range

    def __repr__(self):
        return f"{self.name} {self.valid_range}"


class Ticket:
    def __init__(self, fields):
        self.fields = fields

    def __repr__(self):
        return str(self.fields)


def parse_rules(rule_strs):
    for rule_str in rule_strs:
        match = RULE_REGEX.match(rule_str)
        if match:
            groups = match.groups()
            name = groups[0]
            valid_range = set(range(int(groups[1]), int(groups[2]) + 1))
            valid_range2 = set(range(int(groups[3]), int(groups[4]) + 1))
            valid_range = valid_range.union(valid_range2)
            yield Rule(name, valid_range)


def parse_ticket(tickets):
    for ticket in tickets:
        if not ticket:
            continue
        yield Ticket([int(x) for x in ticket.split(",")])


def parse_input():
    rule_strs = []
    rules = []
    your_ticket = None
    nearby_tickets = []
    ticket_strs = []
    your_ticket_strs = []

    with open("input", "r") as f:
        stage = 0
        for x in f:
            x = x.strip()
            if x == "":
                continue
            if stage == 0 and x != "your ticket:":
                rule_strs.append(x)
            elif stage == 1 and x != "nearby tickets:":
                your_ticket_strs.append(x)
            elif stage == 2:
                ticket_strs.append(x)
            elif x == "your ticket:":
                stage = 1
            elif x == "nearby tickets:":
                stage = 2
            else:
                raise ValueError(f"Unknown input {x}")
    rules = list(parse_rules(rule_strs))
    your_ticket = list(parse_ticket(your_ticket_strs))[0]
    nearby_tickets = list(parse_ticket(ticket_strs))
    return rules, your_ticket, nearby_tickets


def part_1(rules, your_ticket, nearby_tickets):
    ticket_scanning_error_rate = 0
    for ticket in nearby_tickets:
        for value in ticket.fields:
            for rule in rules:
                # print(f"Checking {value} vs {rule}")
                if rule.is_valid(value):
                    # print("Passed")
                    break
            else:
                # print(ticket_scanning_error_rate, value)
                ticket_scanning_error_rate += value
                continue
    return ticket_scanning_error_rate


def part_2(rules, your_ticket, nearby_tickets):
    valid_tickets = []
    for ticket in nearby_tickets:
        valid = True
        for value in ticket.fields:
            for rule in rules:
                if rule.is_valid(value):
                    break
            else:
                valid = False
                continue
        if valid:
            valid_tickets.append(ticket)

    # As our ticket is valid, use it to determine possibles
    possible_positions = {}
    for position, field in enumerate(your_ticket.fields):
        for rule in rules:
            if all(
                [rule.is_valid(ticket.fields[position]) for ticket in valid_tickets]
            ):
                possible_positions.setdefault(position, list()).append(rule)

    # Find all the fields that are currently unique, we can remove them from the problem
    uniques = [pos[0] for pos in possible_positions.values() if len(pos) == 1]

    # Basically sudoku solve: We know a bunch have to be things
    # So take those out of the others, and solve 1 by 1 until we have all of
    # them as unique.
    while len(uniques) != len(possible_positions):
        for unique in uniques:
            for val in possible_positions.values():
                if len(val) > 1 and unique in val:
                    val.remove(unique)
        uniques = [pos[0] for pos in possible_positions.values() if len(pos) == 1]

    # get the deperatues
    departure_values = [
        your_ticket.fields[k]
        for k, v in possible_positions.items()
        if DEPART in v[0].name
    ]
    return math.prod(departure_values)


if __name__ == "__main__":
    rules, your_ticket, nearby_tickets = parse_input()
    print(f"Part 1: error_rate {part_1(rules, your_ticket, nearby_tickets)}")
    print(f"Part 2: deperature values {part_2(rules, your_ticket, nearby_tickets)}")
