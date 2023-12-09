from unittest import TestCase
import answer

CUPS = "389125467"


class TestIntegration(TestCase):
    def setUp(self):
        self.cups = [answer.Cup(x) for x in CUPS]

    def test_part_1(self):
        self.assertEqual(answer.part1(self.cups, debug=False, moves=10), "92658374")

    def test_part_1_100moves(self):
        self.assertEqual(answer.part1(self.cups, debug=False, moves=100), "67384529")

    def test_part_2(self):
        self.assertEqual(answer.part2(self.cups, debug=False), 149245887792)
