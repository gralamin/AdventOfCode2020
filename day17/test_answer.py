from unittest import TestCase
import answer


class TestIntegration(TestCase):
    def test_part_1(self):
        input_state = answer.CubeGrid3D(
            [
                answer.ConwayCube(
                    answer.Coordinate3D(1, 0, 0), answer.CubeState.ACTIVE
                ),
                answer.ConwayCube(
                    answer.Coordinate3D(2, 1, 0), answer.CubeState.ACTIVE
                ),
                answer.ConwayCube(
                    answer.Coordinate3D(0, 2, 0), answer.CubeState.ACTIVE
                ),
                answer.ConwayCube(
                    answer.Coordinate3D(1, 2, 0), answer.CubeState.ACTIVE
                ),
                answer.ConwayCube(
                    answer.Coordinate3D(2, 2, 0), answer.CubeState.ACTIVE
                ),
            ]
        )
        answer.part_1(input_state, num_cycles=3, debug=True)
        self.assertEqual(answer.part_1(input_state, num_cycles=6, debug=False), 112)
