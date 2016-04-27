import sys
import time

path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
sys.path.append(path)
sys.path.append("/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/")

from mySokobanSolver import SokobanPuzzle, checkActions, tabooCells, solveSokoban_elementary, testSolver
from cab320_sokoban import Warehouse

s = SokobanPuzzle(path + "/warehouse_07.txt")
# w = Warehouse()
# w.read_warehouse_file(file_warehouse_07)

t = tabooCells(path + "/warehouse_07.txt")
# t1 = tabooCells(path + "/warehouse_09.txt")
# t2 = tabooCells(path + "/warehouse_55.txt")
# t3 = tabooCells(path + "/warehouse_83.txt")
# t4 = tabooCells(path + "/warehouse_139.txt")
# t5 = tabooCells(path + "/warehouse_89.txt")
# t6 = tabooCells(path + "/warehouse_121.txt")
# t7 = tabooCells(path + "/warehouse_137.txt")
# t8 = tabooCells(path + "/warehouse_077.txt")
# t9 = tabooCells(path + "/warehouse_141.txt")

# print checkActions(file_warehouse_07, ["Right", "Up", "Up", "Left", "Left", "Left", "Up", "Left", "Down", "Down",
#                    "Right", "Down", "Left", "Left"])


# A star
# print "Running A star..."
# t0 = time.time()
# soln_astar = solveSokoban_elementary(path + "/warehouse_07.txt")
# actions_astar = s.print_solution(soln_astar)
# t1 = time.time()
# print "Solver took ", t1-t0, " seconds"
#
# # UCS
# # print "Running UCS"
# # soln_ucs = testSolver(path + "/warehouse_07.txt")
# # actions_ucs = s.print_solution(soln_ucs)
#
# print checkActions(path + "/warehouse_07.txt", actions_astar)
# # print checkActions(path + "/warehouse_07.txt", actions_ucs)
#
# print len(actions_astar)
# # print len(actions_ucs)
#

