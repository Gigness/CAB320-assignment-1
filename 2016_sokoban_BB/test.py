import sys

path_warehouses = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
sys.path.append(path_warehouses)
sys.path.append("/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/")

from mySokobanSolver import SokobanPuzzle, checkActions, tabooCells, solveSokoban_elementary
from cab320_sokoban import Warehouse

s = SokobanPuzzle(path_warehouses + "/warehouse_03.txt")
# w = Warehouse()
# w.read_warehouse_file(file_warehouse_03)

t = tabooCells(path_warehouses + "/warehouse_03.txt")
# t1 = tabooCells(path_warehouses + "/warehouse_09.txt")
# t2 = tabooCells(path_warehouses + "/warehouse_55.txt")
# t3 = tabooCells(path_warehouses + "/warehouse_83.txt")
# t4 = tabooCells(path_warehouses + "/warehouse_139.txt")
# t5 = tabooCells(path_warehouses + "/warehouse_89.txt")
# t6 = tabooCells(path_warehouses + "/warehouse_121.txt")
# t7 = tabooCells(path_warehouses + "/warehouse_137.txt")
# t8 = tabooCells(path_warehouses + "/warehouse_197.txt")
# t9 = tabooCells(path_warehouses + "/warehouse_141.txt")

# print checkActions(file_warehouse_03, ["Right", "Up", "Up", "Left", "Left", "Left", "Up", "Left", "Down", "Down",
#                    "Right", "Down", "Left", "Left"])

# solveSokoban_elementary(path_warehouses + "/warehouse_03.txt")

