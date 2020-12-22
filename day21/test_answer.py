from unittest import TestCase
import answer

EXAMPLE_INPUTS = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


class TestIntegration(TestCase):
    def setUp(self):
        self.foods = [answer.Food(x) for x in EXAMPLE_INPUTS.split("\n")]

    def test_part_1(self):
        self.assertEqual(answer.part1(self.foods), 5)

    def test_part_2(self):
        self.assertEqual(answer.part2(self.foods), "mxmxvkd,sqjhc,fvjkl")
