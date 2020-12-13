from unittest import TestCase
import answer


class TestIntegration(TestCase):
    def setUp(self):
        self.buses = "7,13,x,x,59,x,31,19".split(",")
        self.start_timestamp = 939

    def test_part_one(self):
        self.assertEqual(answer.part_1(self.start_timestamp, self.buses), 295)
