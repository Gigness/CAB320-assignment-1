import sys
import time

path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
sys.path.append(path)
sys.path.append("/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/")

from mySokobanSolver import SokobanPuzzle, checkActions, tabooCells, solveSokoban_elementary, testSolver\
    , SokobanPuzzleMacro
from cab320_sokoban import Warehouse
from cab320_search import ida_star_search, Node

s = SokobanPuzzle(path + "/warehouse_03.txt")

s1 = SokobanPuzzleMacro(path + "/warehouse_03.txt")
s2 = SokobanPuzzleMacro(path + "/warehouse_05.txt")
s3 = SokobanPuzzleMacro(path + "/warehouse_33.txt")
s4 = SokobanPuzzleMacro(path + "/warehouse_69.txt")

# w = Warehouse()
# w.read_warehouse_file(file_warehouse_03)

t = tabooCells(path + "/warehouse_69.txt")
# print t


# print s3.taboo

# t1 = tabooCells(path + "/warehouse_09.txt")
# t2 = tabooCells(path + "/warehouse_55.txt")
# t3 = tabooCells(path + "/warehouse_83.txt")
# t4 = tabooCells(path + "/warehouse_139.txt")
# t5 = tabooCells(path + "/warehouse_89.txt")
# t6 = tabooCells(path + "/warehouse_121.txt")
# t7 = tabooCells(path + "/warehouse_137.txt")
# t8 = tabooCells(path + "/warehouse_037.txt")
# t9 = tabooCells(path + "/warehouse_141.txt")

# print checkActions(file_warehouse_03, ["Right", "Up", "Up", "Left", "Left", "Left", "Up", "Left", "Down", "Down",
#                    "Right", "Down", "Left", "Left"])

# macro action testing for warehouse_33
# print s3.initial
# print s3.__get_macro_end_points__((5,3), (6,4), [(5,3), (3,4), (3,3)])

# test worker_adjacent_to_moveable_box

if False:
    state = s1.initial
    state = list(state)
    worker = state.pop(0)
    print s1.worker_adjacent_to_move_able_box((8,3), state)

if False:
    state = s4.initial
    state = list(state)
    worker = state.pop(0)

    print worker
    print state

    print s4.worker_adjacent_to_move_able_box(worker, state)
    print s4.worker_adjacent_to_move_able_box((8,4), state)
    print s4.worker_adjacent_to_move_able_box((9,3), state)