from unittest import TestCase
from cab320_sokoban import Warehouse
from mySokobanSolver import SokobanPuzzle, checkActions

warehouse_path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses/"
file_warehouse_03 = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses/warehouse_03.txt"

class TestSokobanPuzzle(TestCase):

    def setUp(self):
        self.s = SokobanPuzzle(file_warehouse_03)

    def test_initial_state(self):
        self.assertEqual(self.s.initial, ((7,5), (7,3), (7,4)))

    def test_actions(self):
        action = self.s.actions(self.s.initial)
        self.assertEqual(action, ['Right'])

    def test_bunch_of_actions(self):
        actions = self.s.actions(((8,5), (7,3), (7,4)))
        self.assertEqual(actions, ['Left', 'Up'])

        actions1 = self.s.actions(((8,4), (7,3), (7,4)))
        self.assertEqual(actions1, ['Down', 'Up'])

        actions2 = self.s.actions(((8,3), (7,3), (7,4)))
        self.assertEqual(actions2, ['Left', 'Down'])

        actions3 = self.s.actions(((6,3), (7,3), (7,4)))
        self.assertEqual(actions3, ['Left', 'Right'])

        actions4 = self.s.actions(((5,3), (7,3), (7,4)))
        self.assertEqual(actions4, ['Left', 'Right', 'Down', 'Up'])

        actions5 = self.s.actions(((5,2), (7,3), (7,4)))
        self.assertEqual(actions5, ['Left', 'Down'])

        actions5 = self.s.actions(((2,5), (7,3), (7,4)))
        self.assertEqual(actions5, ['Right', 'Up'])

    def test_goal(self):
        goal = self.s.goal_test(((2,5), (3, 5), (5, 5)))
        self.assertTrue(goal)

    def test_result(self):
        actions = self.s.actions(self.s.initial)
        newState = self.s.result(self.s.initial, actions[0])
        self.assertEquals(newState, ((8, 5), (7, 3), (7, 4)))

        # complex action

        action = 'Left'
        newState1 = self.s.result(((8, 3), (7, 3), (7, 4)), action)
        self.assertEqual(newState1, ((7, 3), (6, 3), (7, 4)))

    def test_taboo_cells(self):
        t = self.s.tabooCells()
        expected = [(4,2), (5,2), (2,3), (8,3), (2,5), (7,5), (8,5)]

        print t
        print expected
        self.assertEqual(t, expected)


