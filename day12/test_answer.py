import answer
import unittest

# Run with: python3 -m unittest


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.inputs = [
            answer.ParsedAction(answer.Actions.FORWARD, 10),
            answer.ParsedAction(answer.Actions.NORTH, 3),
            answer.ParsedAction(answer.Actions.FORWARD, 7),
            answer.ParsedAction(answer.Actions.RIGHT, 90),
            answer.ParsedAction(answer.Actions.FORWARD, 11),
        ]

    def test_part1(self):
        self.assertEqual(answer.part1(self.inputs), 25)

    def test_part2(self):
        self.assertEqual(answer.part2(self.inputs), 286)


class TestDirection(unittest.TestCase):
    def test_turn_left_0(self):
        for direction in answer.Direction:
            self.assertEqual(
                direction.turn_left(0),
                direction,
                "{direction} tried to turn at 0 degrees",
            )

    def test_turn_left_360(self):
        for direction in answer.Direction:
            self.assertEqual(
                direction.turn_left(360),
                direction,
                "{direction} tried to turn at 360 degrees",
            )

    def test_turn_left_90(self):
        expected_map = {
            answer.Direction.EAST: answer.Direction.NORTH,
            answer.Direction.NORTH: answer.Direction.WEST,
            answer.Direction.WEST: answer.Direction.SOUTH,
            answer.Direction.SOUTH: answer.Direction.EAST,
        }
        for direction in answer.Direction:
            self.assertEqual(direction.turn_left(90), expected_map[direction])

    def test_turn_left_180(self):
        expected_map = {
            answer.Direction.EAST: answer.Direction.WEST,
            answer.Direction.NORTH: answer.Direction.SOUTH,
            answer.Direction.WEST: answer.Direction.EAST,
            answer.Direction.SOUTH: answer.Direction.NORTH,
        }
        for direction in answer.Direction:
            self.assertEqual(direction.turn_left(180), expected_map[direction])

    def test_turn_left_270(self):
        expected_map = {
            answer.Direction.EAST: answer.Direction.SOUTH,
            answer.Direction.NORTH: answer.Direction.EAST,
            answer.Direction.WEST: answer.Direction.NORTH,
            answer.Direction.SOUTH: answer.Direction.WEST,
        }
        for direction in answer.Direction:
            self.assertEqual(direction.turn_left(270), expected_map[direction])

    def test_turn_right_0(self):
        for direction in answer.Direction:
            self.assertEqual(
                direction.turn_right(0),
                direction,
                "{direction} tried to turn at 0 degrees",
            )

    def test_turn_right_360(self):
        for direction in answer.Direction:
            self.assertEqual(
                direction.turn_right(360),
                direction,
                "{direction} tried to turn at 360 degrees",
            )

    def test_turn_right_90(self):
        expected_map = {
            answer.Direction.EAST: answer.Direction.SOUTH,
            answer.Direction.NORTH: answer.Direction.EAST,
            answer.Direction.WEST: answer.Direction.NORTH,
            answer.Direction.SOUTH: answer.Direction.WEST,
        }
        for direction in answer.Direction:
            self.assertEqual(direction.turn_right(90), expected_map[direction])

    def test_turn_right_180(self):
        expected_map = {
            answer.Direction.EAST: answer.Direction.WEST,
            answer.Direction.NORTH: answer.Direction.SOUTH,
            answer.Direction.WEST: answer.Direction.EAST,
            answer.Direction.SOUTH: answer.Direction.NORTH,
        }
        for direction in answer.Direction:
            self.assertEqual(direction.turn_right(180), expected_map[direction])

    def test_turn_right_270(self):
        expected_map = {
            answer.Direction.EAST: answer.Direction.NORTH,
            answer.Direction.NORTH: answer.Direction.WEST,
            answer.Direction.WEST: answer.Direction.SOUTH,
            answer.Direction.SOUTH: answer.Direction.EAST,
        }
        for direction in answer.Direction:
            self.assertEqual(direction.turn_right(270), expected_map[direction])

    def test_turn_error(self):
        for direction in answer.Direction:
            self.assertRaises(ValueError, direction.turn_left, 1)
            self.assertRaises(ValueError, direction.turn_right, 1)


class TestCoordinate(unittest.TestCase):

    """
    Grid is defined as so:
                3
                2
                1
    -3  -2  -1  0   1   2   3
               -1
               -2
               -3

    So going west should be negative
    Going east should be positive
    going north should be positive
    going south should be negative
    """

    def setUp(self):
        self.coordinate = answer.Coordinate(0, 0)

    def test_eq(self):
        self.assertEqual(self.coordinate, answer.Coordinate(0, 0))

    def test_neq(self):
        self.assertNotEqual(self.coordinate, answer.Coordinate(0, 1))
        self.assertNotEqual(self.coordinate, answer.Coordinate(0, -1))
        self.assertNotEqual(self.coordinate, answer.Coordinate(1, 0))
        self.assertNotEqual(self.coordinate, answer.Coordinate(-1, 0))
        self.assertNotEqual(self.coordinate, answer.Coordinate(-1, -1))
        self.assertNotEqual(self.coordinate, answer.Coordinate(1, 1))

    def test_add(self):
        self.assertEqual(
            answer.Coordinate(1, 3) + answer.Coordinate(5, -6), answer.Coordinate(6, -3)
        )

    def test_mult(self):
        self.assertEqual(answer.Coordinate(1, 3) * 3, answer.Coordinate(3, 9))

    def test_north(self):
        self.assertEqual(self.coordinate.north(5), answer.Coordinate(0, 5))

    def test_south(self):
        self.assertEqual(self.coordinate.south(5), answer.Coordinate(0, -5))

    def test_east(self):
        self.assertEqual(self.coordinate.east(5), answer.Coordinate(5, 0))

    def test_west(self):
        self.assertEqual(self.coordinate.west(5), answer.Coordinate(-5, 0))

    def test_manhanttan_distance(self):
        self.assertEqual(
            self.coordinate.manhanttan_distance(answer.Coordinate(17, -8)), 25
        )


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = answer.Ship()

    def test_ship_east(self):
        self.ship.do_action(answer.Actions.EAST, 5)
        self.assertEqual(self.ship.position, answer.Coordinate(5, 0))
        self.assertEqual(self.ship.facing, answer.Direction.EAST)

    def test_ship_west(self):
        self.ship.do_action(answer.Actions.WEST, 5)
        self.assertEqual(self.ship.position, answer.Coordinate(-5, 0))
        self.assertEqual(self.ship.facing, answer.Direction.EAST)

    def test_ship_north(self):
        self.ship.do_action(answer.Actions.NORTH, 5)
        self.assertEqual(self.ship.position, answer.Coordinate(0, 5))
        self.assertEqual(self.ship.facing, answer.Direction.EAST)

    def test_ship_south(self):
        self.ship.do_action(answer.Actions.SOUTH, 5)
        self.assertEqual(self.ship.position, answer.Coordinate(0, -5))
        self.assertEqual(self.ship.facing, answer.Direction.EAST)

    def test_ship_deafult_forward(self):
        self.ship.do_action(answer.Actions.FORWARD, 5)
        self.assertEqual(self.ship.position, answer.Coordinate(5, 0))
        self.assertEqual(self.ship.facing, answer.Direction.EAST)

    def test_ship_left(self):
        self.ship.do_action(answer.Actions.LEFT, 90)
        self.assertEqual(self.ship.position, answer.Coordinate(0, 0))
        self.assertEqual(self.ship.facing, answer.Direction.NORTH)

    def test_ship_right(self):
        self.ship.do_action(answer.Actions.RIGHT, 90)
        self.assertEqual(self.ship.position, answer.Coordinate(0, 0))
        self.assertEqual(self.ship.facing, answer.Direction.SOUTH)

    def test_ship_waypoint_right_90(self):
        self.ship.waypoint = answer.Coordinate(5, 5)
        self.ship.do_action_waypoint(answer.Actions.RIGHT, 90)
        # To roate right around 0,0 we change from the top right quandrant,
        #  to the bottom right quadrant so y changes
        self.assertEqual(self.ship.waypoint, answer.Coordinate(5, -5))
        self.ship.do_action_waypoint(answer.Actions.RIGHT, 90)
        # To roate right around 0,0 we change from the bottom right quandrant,
        #  to the bottom left quadrant so x changes
        self.assertEqual(self.ship.waypoint, answer.Coordinate(-5, -5))
        self.ship.do_action_waypoint(answer.Actions.RIGHT, 90)
        # To roate right around 0,0 we change from the bottom left quandrant,
        # to the top left quadrant so y changes
        self.assertEqual(self.ship.waypoint, answer.Coordinate(-5, 5))
        self.ship.do_action_waypoint(answer.Actions.RIGHT, 90)
        # To roate right around 0,0 we change from the top left quandrant,
        # to the top right quadrant, so x changes
        self.assertEqual(self.ship.waypoint, answer.Coordinate(5, 5))

    def test_ship_waypoint_right_werid_degrees(self):
        self.ship.waypoint = answer.Coordinate(5, 5)
        self.ship.do_action_waypoint(answer.Actions.RIGHT, 20)
        self.assertEqual(self.ship.waypoint, answer.Coordinate(6, 3))
        self.ship.do_action_waypoint(answer.Actions.RIGHT, 30)
        self.assertEqual(self.ship.waypoint, answer.Coordinate(7, 0))
        self.ship.do_action_waypoint(answer.Actions.RIGHT, 40)
        # Although at 90, we have hit multiple rounding errors.
        self.assertEqual(self.ship.waypoint, answer.Coordinate(5, -4))

        # Correct rounding errors.
        self.ship.waypoint = answer.Coordinate(5, -5)

        self.ship.do_action_waypoint(answer.Actions.RIGHT, 132)
        self.assertEqual(self.ship.waypoint, answer.Coordinate(-7, 0))
        self.ship.do_action_waypoint(answer.Actions.RIGHT, 49)
        self.assertEqual(self.ship.waypoint, answer.Coordinate(-5, 5))

    def test_ship_waypoint_left_90(self):
        # See logic for right, but reverse it.
        self.ship.waypoint = answer.Coordinate(5, 5)
        self.ship.do_action_waypoint(answer.Actions.LEFT, 90)
        self.assertEqual(self.ship.waypoint, answer.Coordinate(-5, 5))
        self.ship.do_action_waypoint(answer.Actions.LEFT, 90)
        self.assertEqual(self.ship.waypoint, answer.Coordinate(-5, -5))
        self.ship.do_action_waypoint(answer.Actions.LEFT, 90)
        self.assertEqual(self.ship.waypoint, answer.Coordinate(5, -5))
        self.ship.do_action_waypoint(answer.Actions.LEFT, 90)
        self.assertEqual(self.ship.waypoint, answer.Coordinate(5, 5))

    def test_ship_toward_waypoint(self):
        self.ship.move_toward_waypoint(5)
        self.assertEqual(self.ship.position, answer.Coordinate(10 * 5, 1 * 5))

    def test_ship_turn_and_forward(self):
        self.ship.do_action(answer.Actions.LEFT, 90)
        self.ship.do_action(answer.Actions.FORWARD, 5)
        self.assertEqual(self.ship.position, answer.Coordinate(0, 5))
        self.assertEqual(self.ship.facing, answer.Direction.NORTH)

    def test_ship_manhattan(self):
        self.assertEqual(self.ship.manhanttan_distance(answer.Coordinate(17, -8)), 25)


class TestActionParser(unittest.TestCase):
    def setUp(self):
        self.parser = answer.ActionParser()

    def test_north(self):
        parsed = self.parser.parse_action("N10\n")
        self.assertEqual(parsed.action, answer.Actions.NORTH)
        self.assertEqual(parsed.number, 10)

    def test_east(self):
        parsed = self.parser.parse_action("E5\n")
        self.assertEqual(parsed.action, answer.Actions.EAST)
        self.assertEqual(parsed.number, 5)

    def test_south(self):
        parsed = self.parser.parse_action("S100000\n")
        self.assertEqual(parsed.action, answer.Actions.SOUTH)
        self.assertEqual(parsed.number, 100000)

    def test_west(self):
        parsed = self.parser.parse_action("W340000\n")
        self.assertEqual(parsed.action, answer.Actions.WEST)
        self.assertEqual(parsed.number, 340000)

    def test_forward(self):
        parsed = self.parser.parse_action("F15\n")
        self.assertEqual(parsed.action, answer.Actions.FORWARD)
        self.assertEqual(parsed.number, 15)

    def test_left(self):
        parsed = self.parser.parse_action("L0\n")
        self.assertEqual(parsed.action, answer.Actions.LEFT)
        self.assertEqual(parsed.number, 0)

    def test_right(self):
        parsed = self.parser.parse_action("R720\n")
        self.assertEqual(parsed.action, answer.Actions.RIGHT)
        self.assertEqual(parsed.number, 720)

    def test_error(self):
        self.assertRaises(ValueError, self.parser.parse_action, "dsdsadasd\n")
