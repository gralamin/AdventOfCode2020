from unittest import TestCase
import answer


class TestIntegration(TestCase):
    def setUp(self):
        self.input_rules = [
            answer.Rule("class", set([1, 2, 3, 5, 6, 7])),
            answer.Rule(
                "row",
                set(
                    [6, 7, 8, 9, 10, 11, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
                ),
            ),
            answer.Rule(
                "seat",
                set(
                    [
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                        27,
                        28,
                        29,
                        30,
                        31,
                        32,
                        33,
                        34,
                        35,
                        36,
                        37,
                        38,
                        39,
                        40,
                        45,
                        46,
                        47,
                        48,
                        49,
                        50,
                    ]
                ),
            ),
        ]
        self.input_your_ticket = answer.Ticket([7, 1, 14])
        self.input_nearby_tickets = [
            answer.Ticket([7, 3, 47]),
            answer.Ticket([40, 4, 50]),
            answer.Ticket([55, 2, 20]),
            answer.Ticket([38, 6, 12]),
        ]

    def test_part_one_example1(self):
        self.assertEqual(
            answer.part_1(
                self.input_rules, self.input_your_ticket, self.input_nearby_tickets
            ),
            71,
        )


class TestIntegrationPart2(TestCase):
    def setUp(self):
        self.input_rules = [
            answer.Rule(
                f"{answer.DEPART} class",
                set([0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]),
            ),
            answer.Rule(
                "row",
                set([0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]),
            ),
            answer.Rule(
                f"{answer.DEPART} seat",
                set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19]),
            ),
        ]
        self.input_your_ticket = answer.Ticket([11, 12, 13])
        self.input_nearby_tickets = [
            answer.Ticket([3, 9, 18]),
            answer.Ticket([15, 1, 5]),
            answer.Ticket([5, 14, 9]),
        ]

    def test_part_two_example(self):
        self.assertEqual(
            answer.part_2(
                self.input_rules, self.input_your_ticket, self.input_nearby_tickets
            ),
            12 * 13,
        )
