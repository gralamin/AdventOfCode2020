from unittest import TestCase
import answer

EXAMPLE_INPUTS_P1 = """Player 1:
9
2
6
3
1"""

EXAMPLE_INPUTS_P2 = """Player 2:
5
8
4
7
10"""

INF_LOOP_P1 = """Player 1:
43
19"""

INF_LOOP_P2 = """Player 2:
2
29
14"""


class TestIntegration(TestCase):
    def setUp(self):
        self.deckp1 = answer.Deck(EXAMPLE_INPUTS_P1)
        self.deckp2 = answer.Deck(EXAMPLE_INPUTS_P2)
        self.inf1 = answer.Deck(INF_LOOP_P1)
        self.inf2 = answer.Deck(INF_LOOP_P2)

    def test_part_1(self):
        self.assertEqual(answer.part1([self.deckp1, self.deckp2]), 306)

    def test_part_2(self):
        self.assertEqual(answer.part2([self.deckp1, self.deckp2], debug=False), 291)

    def test_part_2_check_infinite(self):
        self.assertEqual(answer.part2([self.inf1, self.inf2], debug=False), 105)
