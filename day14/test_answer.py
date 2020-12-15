from unittest import TestCase
import answer


class TestIntegration(TestCase):
    def setUp(self):
        self.instructions = [
            answer.Instruction(
                answer.InstructionType.MASK,
                None,
                "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
            ),
            answer.Instruction(answer.InstructionType.MEM, 8, 11),
            answer.Instruction(answer.InstructionType.MEM, 7, 101),
            answer.Instruction(answer.InstructionType.MEM, 8, 0),
        ]

    def test_part_one(self):
        self.assertEqual(answer.part_1(self.instructions), 165)

    def test_part_one_real_input(self):
        self.assertEqual(answer.part_1(answer.get_instructions()), 11501064782628)
