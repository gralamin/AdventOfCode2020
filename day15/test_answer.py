from unittest import TestCase
import answer


class TestIntegration(TestCase):
    def test_part_one_example1(self):
        self.assertEqual(answer.part_1([0, 3, 6]), 436)

    def test_part_one_example2(self):
        self.assertEqual(answer.part_1([1, 3, 2]), 1)

    def test_part_one_example3(self):
        self.assertEqual(answer.part_1([2, 1, 3]), 10)

    def test_part_one_example4(self):
        self.assertEqual(answer.part_1([1, 2, 3]), 27)

    def test_part_one_example5(self):
        self.assertEqual(answer.part_1([2, 3, 1]), 78)

    def test_part_one_example6(self):
        self.assertEqual(answer.part_1([3, 2, 1]), 438)

    def test_part_one_example7(self):
        self.assertEqual(answer.part_1([3, 1, 2]), 1836)

    def test_part_two_example1(self):
        self.assertEqual(answer.part_2([0, 3, 6]), 175594)

    def test_part_two_example2(self):
        self.assertEqual(answer.part_2([1, 3, 2]), 2578)

    def test_part_two_example3(self):
        self.assertEqual(answer.part_2([2, 1, 3]), 3544142)

    def test_part_two_example4(self):
        self.assertEqual(answer.part_2([1, 2, 3]), 261214)

    def test_part_two_example5(self):
        self.assertEqual(answer.part_2([2, 3, 1]), 6895259)

    def test_part_two_example6(self):
        self.assertEqual(answer.part_2([3, 2, 1]), 18)

    def test_part_two_example7(self):
        self.assertEqual(answer.part_2([3, 1, 2]), 362)
