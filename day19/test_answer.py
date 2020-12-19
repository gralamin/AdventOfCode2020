from unittest import TestCase
import answer


class TestIntegration(TestCase):
    def test_part_1(self):
        rules = [
            answer.Rule("0: 4 1 5"),
            answer.Rule("1: 2 3 | 3 2"),
            answer.Rule("2: 4 4 | 5 5"),
            answer.Rule("3: 4 5 | 5 4"),
            answer.Rule('4: "a"'),
            answer.Rule('5: "b"'),
        ]
        messages = ["ababbb", "bababa", "abbbab", "aaabbb", "aaaabbb"]
        self.assertEqual(answer.part1(rules, messages), 2)
