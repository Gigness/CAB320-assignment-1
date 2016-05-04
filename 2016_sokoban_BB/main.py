from mySokobanSolver import *
import time


def main():
    path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
    warehouse = path + "/warehouse_43.txt"

    s = SokobanPuzzle(warehouse)

    print s.taboo

    t0 = time.time()
    sol = solveSokoban_elementary(warehouse)

    t1 = time.time()

    actions = s.print_solution(sol)

    print checkActions(warehouse, actions)
    print "Solver took ", t1-t0, " seconds"


def macro():
    path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
    warehouse = path + "/warehouse_35.txt"
    s = SokobanPuzzleMacro(warehouse)

    # print s.taboo

    t0 = time.time()
    sol = solveSokoban_macro(warehouse)
    t1 = time.time()

    print sol

    actions = s.print_solution(sol)
    #
    print checkActions(warehouse, actions)
    print "Solver took ", t1-t0, " seconds"


def macro_ida_star():
    path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
    warehouse = path + "/warehouse_09.txt"
    s = SokobanPuzzleMacro(warehouse)

    # print s.taboo

    t0 = time.time()
    sol = test_solver(warehouse)
    t1 = time.time()

    print sol

    actions = s.print_solution(sol)

    print checkActions(warehouse, actions)
    print "Solver took ", t1-t0, " seconds"

if __name__ == "__main__":
    macro()
    # main()
    # macro_ida_star()
