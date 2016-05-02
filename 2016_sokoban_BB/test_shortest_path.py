import sys
import time

path = "/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/warehouses"
sys.path.append(path)
sys.path.append("/Users/Gigness/CAB320/assignment_one/2016_sokoban_bb/")

from mySokobanSolver import SokobanPuzzle, checkActions, tabooCells, solveSokoban_elementary, testSolver\
    , SokobanPuzzleMacro, ShortestPath

from cab320_search import astar_search


if True:
    s1 = SokobanPuzzleMacro(path + "/warehouse_69.txt")

    initial_state = list(s1.initial)
    worker = initial_state.pop(0)
    state = tuple(initial_state)
    box1 = state[0]
    box2 = state[1]
    box3 = state[2]

    target_locations = s1.get_macro_end_points(box3, worker, state)
    sub1 = ShortestPath(worker, s1.warehouse.walls, state, target_locations[0])

    print "worker: ", worker, ", box1: ", box3, ", target_loc: ", target_locations

    sol = astar_search(sub1)

    # if sol is not None:
    #     for node in sol.path():
    #         print node.action
    # else:
    #     "** No path to target **"

    actions = s1.sub_problem_actions(sol)
    print actions

