import sys

path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/"
path_warehouses = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
file_warehouse_03 = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses/warehouse_03.txt"
sys.path.append(path)
sys.path.append(path_warehouses)

from mySokobanSolver import SokobanPuzzle
from cab320_sokoban import Warehouse

soko = SokobanPuzzle(file_warehouse_03)
w = Warehouse()
w.read_warehouse_file(file_warehouse_03)
