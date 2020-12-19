from unittest import TestCase
import answer


class TestIntegration(TestCase):
    def test_part_1(self):
        expressions = {
            "1 + 2 * 3 + 4 * 5 + 6": 71,
            "1 + (2 * 3) + (4 * (5 + 6))": 51,
            "2 * 3 + (4 * 5)": 26,
            "5 + (8 * 3 + 9 + 3 * 4 * 3)": 437,
            "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))": 12240,
            "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2": 13632,
        }
        for expression, result in expressions.items():
            self.assertEqual(answer.part1([expression]), result)

        self.assertEqual(answer.part1(expressions.keys()), sum(expressions.values()))
