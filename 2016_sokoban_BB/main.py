from mySokobanSolver import *
import time


def main():
    path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
    s = SokobanPuzzle(path + "/warehouse_69.txt")

    print s.taboo

    t0 = time.time()
    sol = solveSokoban_elementary(path + "/warehouse_71.txt")

    t1 = time.time()

    actions = s.print_solution(sol)

    print checkActions(path + "/warehouse_71.txt", actions)
    print "Solver took ", t1-t0, " seconds"


def macro():
    path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
    s = SokobanPuzzleMacro(path + "/warehouse_03.txt")

    # print s.taboo

    t0 = time.time()
    sol = solveSokoban_macro(path + "/warehouse_03.txt")
    t1 = time.time()

    print sol

    actions = s.print_solution(sol)
    #
    # print checkActions(path + "/warehouse_69.txt", actions)
    print "Solver took ", t1-t0, " seconds"

if __name__ == "__main__":
    macro()
    # main()
