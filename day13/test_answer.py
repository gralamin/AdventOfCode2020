from unittest import TestCase
import answer


class TestIntegration(TestCase):
    def setUp(self):
        self.buses = "7,13,x,x,59,x,31,19".split(",")
        self.start_timestamp = 939

    def test_part_one(self):
        self.assertEqual(answer.part_1(self.start_timestamp, self.buses), 295)

    def test_part_two(self):
        self.assertEqual(answer.part_2(self.buses), 1068781)

    def test_part_two_other_examples(self):
        self.assertEqual(answer.part_2("17,x,13,19".split(",")), 3417)
        self.assertEqual(answer.part_2("67,7,59,61".split(",")), 754018)
        self.assertEqual(answer.part_2("67,x,7,59,61".split(",")), 779210)
        self.assertEqual(answer.part_2("67,7,x,59,61".split(",")), 1261476)
        self.assertEqual(answer.part_2("1789,37,47,1889".split(",")), 1202161486)
