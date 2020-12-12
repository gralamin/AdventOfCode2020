from enum import Enum
import re
from collections import namedtuple


class Direction(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    def turn_left(self, number):
        if number == 0:
            return self
        if number % 90 != 0:
            raise ValueError("Non-90 degree turn, unhandled")
        number = number - 90
        if self == self.NORTH:
            return self.WEST.turn_left(number)
        elif self == self.EAST:
            return self.NORTH.turn_left(number)
        elif self == self.SOUTH:
            return self.EAST.turn_left(number)
        elif self == self.WEST:
            return self.SOUTH.turn_left(number)
        else:
            raise ValueError("Don't know how to turn left from {self}")

    def turn_right(self, number):
        if number == 0:
            return self
        if number % 90 != 0:
            raise ValueError("Non-90 degree turn, unhandled")
        number = number - 90
        if self == self.NORTH:
            return self.EAST.turn_right(number)
        elif self == self.EAST:
            return self.SOUTH.turn_right(number)
        elif self == self.SOUTH:
            return self.WEST.turn_right(number)
        elif self == self.WEST:
            return self.NORTH.turn_right(number)
        else:
            raise ValueError("Don't know how to turn right from {self}")


class Actions(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    LEFT = "L"
    RIGHT = "R"
    FORWARD = "F"


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def north(self, num_north):
        return Coordinate(self.x, self.y + num_north)

    def south(self, num_south):
        return Coordinate(self.x, self.y - num_south)

    def east(self, num_east):
        return Coordinate(self.x + num_east, self.y)

    def west(self, num_west):
        return Coordinate(self.x - num_west, self.y)

    def manhanttan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


# Define starting point as 0
STARTING_POSITION = Coordinate(0, 0)


class Ship:
    def __init__(self):
        self.facing = Direction.EAST
        self.position = STARTING_POSITION

    def do_action(self, action, number):
        if action == Actions.NORTH:
            self.position = self.position.north(number)
        elif action == Actions.EAST:
            self.position = self.position.east(number)
        elif action == Actions.SOUTH:
            self.position = self.position.south(number)
        elif action == Actions.WEST:
            self.position = self.position.west(number)
        elif action == Actions.LEFT:
            self.facing = self.facing.turn_left(number)
        elif action == Actions.RIGHT:
            self.facing = self.facing.turn_right(number)
        elif action == Actions.FORWARD:
            self.move_forward(number)
        else:
            raise ValueError(f"Unknown action {action}")

    def move_forward(self, number):
        if self.facing == Direction.EAST:
            self.position = self.position.east(number)
        elif self.facing == Direction.SOUTH:
            self.position = self.position.south(number)
        elif self.facing == Direction.WEST:
            self.position = self.position.west(number)
        elif self.facing == Direction.NORTH:
            self.position = self.position.north(number)
        else:
            raise ValueError(f"Unknown direction {self.facing}")

    def __str__(self):
        return f"{type(self).__name__} facing {self.facing}, at {self.position}"

    def __repr__(self):
        return str(self)

    def manhanttan_distance(self, coordinate):
        return self.position.manhanttan_distance(coordinate)


ParsedAction = namedtuple("ParsedAction", ["action", "number"])


class ActionParser:
    def __init__(self):
        self.possible_actions = []
        for action in Actions:
            self.possible_actions.append(action.value)
        actions_list = "".join(self.possible_actions)
        self.regex = re.compile(f"^([{actions_list}])(\\d+)$")

    def parse_action(self, input_str):
        match = self.regex.match(input_str.strip())
        if not match:
            raise ValueError(f"Cannot parse {input_str}")
        groups = match.groups()
        action_char = groups[0]
        number = groups[1]
        return ParsedAction(Actions(action_char), int(number))


def get_inputs(filename="input"):
    parser = ActionParser()
    actions = []
    with open(filename, "r") as f:
        actions = [parser.parse_action(x) for x in f if x.strip() != "\n"]
    return actions


def part1(parsed_actions):
    ship = Ship()
    for parsed_action in parsed_actions:
        ship.do_action(parsed_action.action, parsed_action.number)
    distance = ship.manhanttan_distance(STARTING_POSITION)
    return distance


if __name__ == "__main__":
    parsed_inputs = get_inputs()
    print("Part 1: ", part1(parsed_inputs))
