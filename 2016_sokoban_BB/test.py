import sys
import time

path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
sys.path.append(path)
sys.path.append("/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/")

from mySokobanSolver import SokobanPuzzle, checkActions, tabooCells, solveSokoban_elementary,\
    SokobanPuzzleMacro
from cab320_search import ida_star_search, Node

s1 = SokobanPuzzleMacro(path + "/warehouse_03.txt")
s2 = SokobanPuzzleMacro(path + "/warehouse_05.txt")
s3 = SokobanPuzzleMacro(path + "/warehouse_33.txt")
s4 = SokobanPuzzleMacro(path + "/warehouse_69.txt")

print tabooCells(path + "/warehouse_37.txt")


