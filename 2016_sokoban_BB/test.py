import sys
import time

path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
sys.path.append(path)
sys.path.append("/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/")

from mySokobanSolver import SokobanPuzzle, checkActions, tabooCells, solveSokoban_elementary, testSolver
from cab320_sokoban import Warehouse
from cab320_search import ida_star_search, Node

s = SokobanPuzzle(path + "/warehouse_03.txt")
# w = Warehouse()
# w.read_warehouse_file(file_warehouse_03)

t = tabooCells(path + "/warehouse_03.txt")
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


# ida star

t0 = time.time()

sol = solveSokoban_elementary(path + "/warehouse_03.txt")

t1 = time.time()

actions = s.print_solution(sol)

print checkActions(path + "/warehouse_03.txt", actions)
print "Solver took ", t1-t0, " seconds"


