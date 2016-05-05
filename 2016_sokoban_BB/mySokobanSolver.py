from cab320_search import Problem, astar_search, ida_star_search
import cab320_sokoban
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(Problem):
    """
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the module  cab320_search

    States are represented using a tuple of the following form:
        ((worker_x, worker_y), (box1_x, box1_y), ... (boxN_x, boxN_y))
        the worker is always in the 0th position
    """

    def __init__(self, puzzleFileName):
        """
        Important instance variables
        warehouse: warehouse representation from cab320_sokoban
        goal: string representation of the goal state
        initial: tuple showing position of the worker and the boxes
            - ((w_x, w_y), (b1_x, b1_y), ..., (bN_x, bN_y))
        taboo: coordinates of the taboo cells

        :param puzzleFileName: warehouse file name to be loaded
        """
        self.warehouse = cab320_sokoban.Warehouse()
        self.warehouse.read_warehouse_file(puzzleFileName)
        self.goal = self.getGoalState()
        # Extract worker and box locations for initial state tuple
        initial = list(self.warehouse.boxes)
        initial.insert(0, self.warehouse.worker)  # Worker at 0 tuple pos
        self.initial = tuple(initial)
        self.taboo = self.getTabooCells()

    def goal_test(self, state):
        """
        Checks whether the given state of boxes are on the targets
        :param state: current state of warehouse
            - first tuple is the worker
            - preceding tuples are boxes
        :return boolean: True or False
        """
        state = list(state)
        del state[0]  # Remove the worker, only need to check boxes
        for box in state:
            if box not in self.warehouse.targets:
                return False
        return True

    def actions(self, state):
        """
        Determines which actions are viable for the worker in the current state.
        Available actions are Left, Right, Up and Down.
            - checks if the worker will move into a wall
            - checks if the worker will be pushing a box
                - if the pushed box will be pushed onto a wall (illegal)
                - if the pushed box will be in a taboo cell (illegal)
                - if the pushed box will be pushed onto another box (illegal)
        :param state: Current state of the warehouse
        :return: actions list of legal actions from the current state
        """
        state = list(state)
        actions = list()

        # Worker positions to check
        (w_x, w_y) = state.pop(0)
        w_x_left = w_x - 1
        w_x_right = w_x + 1
        w_y_up = w_y - 1
        w_y_down = w_y + 1

        # check if a left move is legal
        if (w_x_left, w_y) not in self.warehouse.walls:  # check walls
            if (w_x_left, w_y) in state:
                (b_x, b_y) = (w_x_left, w_y)
                b_x_left = b_x - 1
                if (b_x_left, b_y) not in self.warehouse.walls and (b_x_left, b_y) not in state\
                        and (b_x_left, b_y) not in self.taboo:  # is the boxed pushing into a taboo/wall/another_box
                    actions.append('Left')
            else:
                actions.append('Left')
        if (w_x_right, w_y) not in self.warehouse.walls:
            if (w_x_right, w_y) in state:
                (b_x, b_y) = (w_x_right, w_y)
                b_x_right = b_x + 1
                if (b_x_right, b_y) not in self.warehouse.walls and (b_x_right, b_y) not in state\
                        and (b_x_right, b_y) not in self.taboo:
                    actions.append('Right')
            else:
                actions.append('Right')
        if (w_x, w_y_down) not in self.warehouse.walls:
            if (w_x, w_y_down) in state:
                (b_x, b_y) = (w_x, w_y_down)
                b_y_down = b_y + 1
                if (b_x, b_y_down) not in self.warehouse.walls and (b_x, b_y_down) not in state\
                        and (b_x, b_y_down) not in self.taboo:
                    actions.append('Down')
            else:
                actions.append('Down')
        if (w_x, w_y_up) not in self.warehouse.walls:
            if (w_x, w_y_up) in state:
                (b_x, b_y) = (w_x, w_y_up)
                b_y_up = b_y - 1
                if (b_x, b_y_up) not in self.warehouse.walls and (b_x, b_y_up) not in state\
                        and (b_x, b_y_up) not in self.taboo:
                    actions.append('Up')
            else:
                actions.append('Up')
        return actions

    def result(self, state, action):
        """
        Given a legal action, return a new state after the action is performed.
        Exception is thrown if unknown action is given.
        The legality of actions are determined in SokobanPuzzle.actions method.
        :param state: current state of the warehouse
        :param action: legal action string (Left, Right, Up, Down)
        :return state: tuple of new warehouse state
        """
        state = list(state)
        (w_x, w_y) = state.pop(0)  # Pop out the worker position

        if action == 'Left':
            w_x1 = w_x - 1
            if (w_x1, w_y) in state:
                (b_x, b_y) = (w_x1, w_y)
                state[state.index((b_x, b_y))] = (b_x - 1, b_y)  # Move pushed box left
            state.insert(0, (w_x1, w_y))  # Insert the worker back into the state

        elif action == 'Right':
            w_x1 = w_x + 1
            if (w_x1, w_y) in state:
                (b_x, b_y) = (w_x1, w_y)
                state[state.index((b_x, b_y))] = (b_x + 1, b_y)  # Move pushed box right
            state.insert(0, (w_x1, w_y))
        elif action == 'Down':
            w_y1 = w_y + 1
            if (w_x, w_y1) in state:
                (b_x, b_y) = (w_x, w_y1)
                state[state.index((b_x, b_y))] = (b_x, b_y + 1)  # Move pushed box left
            state.insert(0, (w_x, w_y1))

        elif action == 'Up':
            w_y1 = w_y - 1
            if (w_x, w_y1) in state:
                (b_x, b_y) = (w_x, w_y1)
                state[state.index((b_x, b_y))] = (b_x, b_y - 1)  # Move pushed box left
            state.insert(0, (w_x, w_y1))
        else:
            raise ValueError("Invalid action given")
        return tuple(state)

    def getGoalState(self):
        """
        Show the goal state of the warehouse.
        :return goalState: string representation of the goal warehouse
        """
        goalState = self.warehouse.visualize()
        goalState = goalState.replace("$", " ").replace(".", "*").replace("@", " ")
        return goalState

    def getTabooCells(self):
        """
        Identify taboo cells in the warehouse by scanning each row 
        and each column for particular characteristics.

        Characteristics of rows and columns which should be marked as taboo:

            1. #XXXXXXX#    Bounded sections (rows)
               #########

            2. #X     X#    Corner sections (rows and columns)
               #####  ##

            3. ###     Bounded sections (columns)
               #X
               #X
               #X
               ###

            4. #X. . .X#    Tricky sections because of targets (rows)
               #########

        The taboo cells method works by:
        1. Determining the start and end coordinates of the walls.
        2. Going through each row starting at the initial + 1 row (because the first row is not accessible).
           Ending at the nth - 1 row (last row is not accessible).
        3. Identifying the walls in the row above, row below and in the current row.
        4. Identifying which positions in the current row are accessible to the boxes (not blocked by walls)
        5. Creates a list of continous accessible segments.
            i.e  current row = #  #   # produces [[2, 3], [5, 6, 7]]
        6. Checks whether each segment forms a "bounded section"
        7. Checks whether the segment has "targets"
        8. Checks for corner sections
        9. Using the characteristics described above, can determine a taboo cell
        10. This is repeated for each column in the warehouse

        :return taboo_targets_removed: tuple of taboo cells
        """
        walls_y = [b for (a,b) in self.warehouse.walls]
        walls_x = [a for (a,b) in self.warehouse.walls]

        walls_x_start = min(walls_x)
        walls_x_end = max(walls_x)

        wall_y_start = min(walls_y)
        wall_y_end = max(walls_y)
        
        taboo = list()

        for row in xrange(wall_y_start + 1, wall_y_end):

            # get the walls above, below and on the current row
            row_above_walls = [a for (a,b) in self.warehouse.walls if b == row - 1]
            row_below_walls = [a for (a,b) in self.warehouse.walls if b == row + 1]
            row_current_walls = [a for (a,b) in self.warehouse.walls if b == row]

            # determine which pos can be accessed by boxes
            accessible_cells = list()

            # determine accessible warehouse positions
            for pos in xrange(row_current_walls[0],row_current_walls[-1] + 1):
                if pos not in row_current_walls:
                    if accessible_cells:  # not empty list
                        if (accessible_cells[-1] != '*') and ((pos - accessible_cells[-1]) != 1):
                            accessible_cells.append('*')
                        accessible_cells.append(pos)
                    else:
                        accessible_cells.append(pos)

            # process the accessible cells sub lists of continuous accessible cells
            accessible_segments = [[]]
            segment = 0

            for cell in accessible_cells:
                if cell == '*':
                    accessible_segments.append([])
                    segment += 1
                else:
                    accessible_segments[segment].append(cell)

            # check if any of the segments are empty, this is bad
            for segment in accessible_segments:
                if not segment:
                    raise ValueError("accessible segment is empty")

            # Begin determining taboo cells
            # Check if the cells are bounded by a U shape
            for segment in accessible_segments:
                bounded_upper_wall = True
                bounded_lower_wall = True
                target_in_segment = False  # Check if there is a target in segment
                for pos in segment:
                    if pos not in row_above_walls:
                        bounded_upper_wall = False
                    if pos not in row_below_walls:
                        bounded_lower_wall = False
                    if (pos, row) in self.warehouse.targets:  # target in segment, don't taboo it
                        target_in_segment = True

                if (bounded_upper_wall or bounded_lower_wall) and not target_in_segment:
                    for pos in segment:
                        taboo.append((pos, row))
                else:
                    for pos in segment:
                        if ((pos - 1) in row_current_walls or (pos + 1) in row_current_walls) and (pos in
                        row_below_walls or pos in row_above_walls):
                            taboo.append((pos, row))

        for col in xrange(walls_x_start + 1, walls_x_end):
            row_left_walls = [b for (a,b) in self.warehouse.walls if a == col - 1]
            row_right_walls = [b for (a,b) in self.warehouse.walls if a == col + 1]
            row_current_walls = [b for (a,b) in self.warehouse.walls if a == col]

            # determine which pos can be accessed by boxes
            accessible_cells = list()

            # determine accessible warehouse positions (y position)
            for pos in xrange(row_current_walls[0],row_current_walls[-1] + 1):
                if pos not in row_current_walls:
                    if accessible_cells:  # not empty list
                        if (accessible_cells[-1] != '*') and ((pos - accessible_cells[-1]) != 1):
                            accessible_cells.append('*')
                        accessible_cells.append(pos)
                    else:
                        accessible_cells.append(pos)

            # process the accessible cells sub lists of continuous accessible cells
            accessible_segments = [[]]
            segment = 0

            for cell in accessible_cells:
                if cell == '*':
                    accessible_segments.append([])
                    segment += 1
                else:
                    accessible_segments[segment].append(cell)

            # check if any of the segments are empty, this is bad
            for segment in accessible_segments:
                if not segment:
                    raise ValueError("accessible segment is empty")

            # Begin determining taboo cells
            # Check if the cells are bounded by a U shape
            for segment in accessible_segments:
                bounded_left_wall = True
                bounded_right_wall = True
                target_in_segment = False  # Check if there is a target in segment
                for pos in segment:
                    if pos not in row_left_walls:
                        bounded_left_wall = False
                    if pos not in row_right_walls:
                        bounded_right_wall = False
                    if (col, pos) in self.warehouse.targets:  # target in segment, don't taboo it
                        target_in_segment = True

                if (bounded_left_wall or bounded_right_wall) and not target_in_segment:
                    for pos in segment:
                        if (col, pos) not in taboo:
                            taboo.append((col, pos))
                else:
                    for pos in segment:
                        if ((pos - 1) in row_current_walls or (pos + 1) in row_current_walls) and (pos in
                        row_left_walls or pos in row_right_walls):
                            if (col,pos) not in taboo:
                                taboo.append((col, pos))

            taboo_targets_removed = [t for t in taboo if t not in self.warehouse.targets]

        return taboo_targets_removed

    def path_cost(self, c, state1, action, state2):
        """
        Calculates path cost.
        For elementary solver this is simply the parent path cost + 1.
        :param c: Parents path cost
        :param state1: Current state
        :param action: action performed
        :param state2: new state
        :return: path cost performing given action from state1 to state2
        """
        return c + 1

    def print_solution(self, goal_node):
        actions = []
        if goal_node == None:
            print "No solution found"
        elif goal_node == 'cuttoff':
            print "cuttoff"
        else:
            # path is list of nodes from initial state (root of the tree)
            # to the goal_node
            path = goal_node.path()
            # print the solution
            print "Solution takes {0} steps from the initial state".format(len(path)-1)
            print path[0].state
            print "to the goal state"
            print path[-1].state
            print "\nBelow is the sequence of moves\n"
            for node in path:
                if node.action is not None:
                    print "{0}".format(node.action)
                # print node.state, " path_cost: ", node.path_cost
                    actions.append(node.action)
            return actions

    def h(self, node):
        """
        Manhattan distances between boxes to targets.
        Calculates minimum distance between a box and the closest target.
        Does not take into account multiple boxes matched to the same target.
        :param node: node containing the state
        :return dist: Total Manhattan distances heuristic
        """

        state = list(node.state)
        state.pop(0)
        dist = 0

        for i in xrange(len(state)):
            dist_each_box = []
            if state[i] not in self.warehouse.targets:  # no point checking the boxes already on targets
                for j in xrange(len(self.warehouse.targets)):
                    b_x, b_y = state[i]
                    t_x, t_y = self.warehouse.targets[j]
                    dist_to_box = abs(b_x - t_x) + abs(b_y - t_y)
                    dist_each_box.append(dist_to_box)
                dist += min(dist_each_box)
        return dist


class SokobanPuzzleMacro(SokobanPuzzle):

    def worker_adjacent_to_move_able_box(self, worker, state_of_boxes):
        """
        This method firstly identifies whether the worker is adjacent to a box.
        If the worker is adjacent to a box, it will check if pushing that box is viable
        and whether it will cause a "dynamic deadlock" state.

        If pushing the box results in a viable state (no deadlocks, walls taboo
        other boxes) then the action is appended to a list.
        Potential actions are Right, Left, Up, Down.


            "dynamic deadlock"

            1.    @      Pushing the box down will lock up all three boxes (Bad move)
                  $
               # $ $
               #######

            2. ##       Special case, pushing the box onto a target (Good move)
               #*
               #.$@
               #


        :param worker: worker coords
        :param state_of_boxes: coordinates of all boxes
        :return meaningful_actions: list of actions which will push the box
        """
        w_x, w_y = worker
        w_x_left = w_x - 1
        w_x_right = w_x + 1
        w_y_up = w_y - 1
        w_y_down = w_y + 1

        # meaningful action means a box is being pushed
        meaningful_actions = []

        if (w_x_left, w_y) in state_of_boxes:  # if left of the worker has a box
            b_x_left = w_x_left - 1
            b_y = w_y

            # check if that box can be moved to the left
            if (b_x_left, b_y) not in self.warehouse.walls and (b_x_left, b_y) not in state_of_boxes\
                    and (b_x_left, b_y) not in self.taboo:

                # Check if moving the box will cause a dynamic dead lock
                adj_box_above = (b_x_left, b_y - 1)
                adj_box_below =(b_x_left, b_y + 1)

                if adj_box_above not in state_of_boxes and adj_box_below not in state_of_boxes:
                    meaningful_actions.append("Left")
                else:

                    dead_lock = False

                    if adj_box_above in state_of_boxes:  # Theres a box adjacent (above)
                        b_adj_above_x, b_adj_above_y = adj_box_above

                        check_wall_adj = b_adj_above_x - 1, b_adj_above_y
                        check_wall_box = b_x_left - 1, b_y

                        if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                            if adj_box_above not in self.warehouse.targets and\
                            (b_x_left, b_y) not in self.warehouse.targets:
                                dead_lock = True

                    if adj_box_below in state_of_boxes:
                        b_adj_below_x, b_adj_below_y = adj_box_below

                        check_wall_adj = b_adj_below_x - 1, b_adj_below_y
                        check_wall_box = b_x_left - 1, b_y

                        if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                            if adj_box_below not in self.warehouse.targets or\
                            (b_x_left, b_y) not in self.warehouse.targets:
                                dead_lock = True
                    if not dead_lock:
                        meaningful_actions.append("Left")
        # check to the right of the worker for a box
        if (w_x_right, w_y) in state_of_boxes:
            # check if that box can be moved
            b_x_right = w_x_right + 1
            b_y = w_y
            if (b_x_right, b_y) not in self.warehouse.walls and (b_x_right, b_y) not in state_of_boxes\
                    and (b_x_right, b_y) not in self.taboo:

                adj_box_above = (b_x_right, b_y - 1)
                adj_box_below = (b_x_right, b_y + 1)

                if adj_box_above not in state_of_boxes and adj_box_below not in state_of_boxes:
                    meaningful_actions.append("Right")
                else:

                    dead_lock = False

                    if adj_box_above in state_of_boxes:  # Theres a box adjacent (above)
                        b_adj_above_x, b_adj_above_y = adj_box_above

                        check_wall_adj = b_adj_above_x + 1, b_adj_above_y
                        check_wall_box = b_x_right + 1, b_y

                        if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                             if adj_box_above not in self.warehouse.targets or\
                            (b_x_right, b_y) not in self.warehouse.targets:
                                dead_lock = True

                    if adj_box_below in state_of_boxes:
                        b_adj_below_x, b_adj_below_y = adj_box_below

                        check_wall_adj = b_adj_below_x + 1, b_adj_below_y
                        check_wall_box = b_x_right + 1, b_y

                        if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                            if adj_box_above not in self.warehouse.targets or\
                            (b_x_right, b_y) not in self.warehouse.targets:
                                dead_lock = True
                    if not dead_lock:
                        meaningful_actions.append("Right")

        if (w_x, w_y_up) in state_of_boxes:
            # check if that box can be moved
            b_x = w_x
            b_y_up = w_y_up - 1
            if (b_x, b_y_up) not in self.warehouse.walls and (b_x, b_y_up) not in state_of_boxes\
                    and (b_x, b_y_up) not in self.taboo:

                adj_box_left = (b_x - 1, b_y_up)
                adj_box_right =(b_x + 1, b_y_up)

                if adj_box_left not in state_of_boxes and adj_box_right not in state_of_boxes:
                    meaningful_actions.append("Up")
                else:

                    dead_lock = False

                    if adj_box_left in state_of_boxes:  # Theres a box adjacent (above)
                        b_adj_left_x, b_adj_left_y = adj_box_left

                        check_wall_adj = b_adj_left_x, b_adj_left_y - 1
                        check_wall_box = b_x, b_y_up - 1

                        if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                            if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                                if adj_box_left not in self.warehouse.targets or\
                                (b_x, b_y_up) not in self.warehouse.targets:
                                    dead_lock = True

                    if adj_box_right in state_of_boxes:
                        b_adj_right_x, b_adj_right_y = adj_box_right

                        check_wall_adj = b_adj_right_x, b_adj_right_y - 1
                        check_wall_box = b_x, b_y_up - 1

                        if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                            if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                                if adj_box_right not in self.warehouse.targets or\
                                (b_x, b_y_up) not in self.warehouse.targets:
                                    dead_lock = True
                    if not dead_lock:
                        meaningful_actions.append("Up")
        if (w_x, w_y_down) in state_of_boxes:
            # check if that box can be moved
            b_x = w_x
            b_y_down = w_y_down + 1
            if (b_x, b_y_down) not in self.warehouse.walls and (b_x, b_y_down) not in state_of_boxes\
                    and (b_x, b_y_down) not in self.taboo:

                adj_box_left = (b_x - 1, b_y_down)
                adj_box_right =(b_x + 1, b_y_down)

                if adj_box_left not in state_of_boxes and adj_box_right not in state_of_boxes:
                    meaningful_actions.append("Down")
                else:

                    dead_lock = False

                    if adj_box_left in state_of_boxes:  # There is a box adjacent (above)
                        b_adj_left_x, b_adj_left_y = adj_box_left

                        check_wall_adj = b_adj_left_x, b_adj_left_y + 1
                        check_wall_box = b_x, b_y_down + 1

                        if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                            if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                                if adj_box_left not in self.warehouse.targets or\
                                (b_x, b_y_down) not in self.warehouse.targets:
                                    dead_lock = True

                    if adj_box_right in state_of_boxes:
                        b_adj_right_x, b_adj_right_y = adj_box_right

                        check_wall_adj = b_adj_right_x, b_adj_right_y + 1
                        check_wall_box = b_x, b_y_down + 1

                        if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                            if check_wall_adj in self.warehouse.walls and check_wall_box in self.warehouse.walls:
                                if adj_box_right not in self.warehouse.targets or\
                                (b_x, b_y_down) not in self.warehouse.targets:
                                    dead_lock = True
                    if not dead_lock:
                        meaningful_actions.append("Down")
        # print meaningful_actions
        return meaningful_actions

    def get_macro_end_points(self, box, worker, state):
        """
        A "macro end point" is a position in the warehouse which is adjacent to a box.
        Identifying "macro end points" will allow for smaller search trees at the cost of greater
        computational complexity when selecting actions.
        In order to determine the viability of each macro end point,
        the position opposite to the end point is analysed.
        This opposite position is where the box will be after the worker has pushed it.
        The opposite position is checked for walls, other boxes, taboo cells and
        whether it will cause a dynamic dead lock.

        "macro end point example"

            #########       The '%' symbols represent macro end points which should
            #     % #       be investigated for their viability.
            #    %$%#
            # @   % #
            #       #
            #########


        :param state: state of the warehouse
        :param box: coords of a moveable box
        :param worker: coords of the worker
        :return: list of "macro end points" for a moveable box
        """

        b_x, b_y = box
        w_x, w_y = worker

        # adjacent box positions
        b_x_left = b_x - 1
        b_x_right = b_x + 1
        b_y_up = b_y - 1
        b_y_down = b_y + 1

        macro_end_point = list()

        # check for walls/boxes to the left and right of the box of interest
        if (b_x_left, b_y) not in self.warehouse.walls and (b_x_left, b_y) not in state\
                and (b_x_right, b_y) not in self.warehouse.walls and (b_x_right, b_y) not in state:

            # if the worker is already next to the box, we don't need a macro action
            if (b_x_left, b_y) != (w_x, w_y):

                # will pushing it right lead to anything?
                if (b_x_right, b_y) not in self.taboo:
                    macro_end_point.append((b_x_left, b_y))  # left of the box

            if (b_x_right, b_y) != (w_x, w_y):

                if (b_x_left, b_y) not in self.taboo:
                    macro_end_point.append((b_x_right, b_y))

        if (b_x, b_y_up) not in self.warehouse.walls and (b_x, b_y_up) not in state\
                and (b_x, b_y_down) not in self.warehouse.walls and (b_x, b_y_down) not in state:

                # if the worker is already next to box, don't need a macro action...
                if (b_x, b_y_up) != (w_x, w_y):

                    # will pushing it down, lead to taboo cell etc?
                    if (b_x, b_y_down) not in self.taboo:
                        macro_end_point.append((b_x, b_y_up))
                if (b_x, b_y_down) != (w_x, w_y):

                    if (b_x, b_y_up) not in self.taboo:
                        macro_end_point.append((b_x, b_y_down))
        return macro_end_point

    def get_macro_actions_list(self, macro_end_point, worker, state):
        """
        Determines an optimal path between the worker and a "macro end point".
        Uses astar search with a manhattan distance heuristc between the worker and the target.
        Refer to the ShortestPath problem class for details.

        :param macro_end_point: target location adjacent to a box
        :param worker: start position of the worker
        :param state: current state of the warehouse
        :return: list of actions or None
        """
        sub_problem = ShortestPath(worker, self.warehouse.walls, state, macro_end_point)
        return astar_search(sub_problem)

    def actions(self, state):
        """
        Identify viable moves for the worker.
        1. Checks if a worker is adjacent to a box and determines if pushing
            that box is viable
        2. Identifies viable "macro end points" for every box and obtains
            the optimal actions in order to move the worker to the end point

        :param state: current warehouse state
        :return: List of viable actions (may include macro or single actions)
        """
        state = list(state)
        actions = list()

        w_x, w_y = state.pop(0)

        # Check if the worker is adjacent to a box, get any viable actions that will push the box
        actions_move_boxes = self.worker_adjacent_to_move_able_box((w_x, w_y), state)

        # if there are any actions which move the box, add it to the list
        if actions_move_boxes:
            for action in actions_move_boxes:
                actions.append(action)

        # Get suitable macro actions to every box
        for box in state:
            macro_end_points = self.get_macro_end_points(box, (w_x, w_y), state)
            # solve the sub problem to get to each macro end point
            if macro_end_points:
                for target_loc in macro_end_points:
                    macro_action = self.get_macro_actions_list(target_loc, (w_x, w_y), state)
                    if macro_action is not None:
                        actions.append(self.unpack_macro_action(macro_action))
        return actions

    def result(self, state, action):
        """
        Given an action (macro or normal), return a new state which reflects the outcome
        of the given action.

        :param state: current state of the warehouse
        :param action: string or a list of strings ("Left", "Right", "Up", "Down")
        :return state: new state of the warehouse
        """

        state = list(state)
        w_x, w_y = state.pop(0)

        # check for a macro action
        if isinstance(action, list):
            for micro_move in action:
                if micro_move == 'Left':
                    w_x -= 1
                elif micro_move == 'Right':
                    w_x += 1
                elif micro_move == 'Up':
                    w_y -= 1
                elif micro_move == 'Down':
                    w_y += 1
                else:
                    raise ValueError("Invalid Micro Move")
            state.insert(0, (w_x, w_y))
        else:
            # perform a single action
            if action == 'Left':
                w_x1 = w_x - 1
                if (w_x1, w_y) in state:
                    (b_x, b_y) = (w_x1, w_y)
                    state[state.index((b_x, b_y))] = (b_x - 1, b_y)  # Move pushed box left
                state.insert(0, (w_x1, w_y))
            elif action == 'Right':
                w_x1 = w_x + 1
                if (w_x1, w_y) in state:
                    (b_x, b_y) = (w_x1, w_y)
                    state[state.index((b_x, b_y))] = (b_x + 1, b_y)  # Move pushed box right
                state.insert(0, (w_x1, w_y))
            elif action == 'Down':
                w_y1 = w_y + 1
                if (w_x, w_y1) in state:
                    (b_x, b_y) = (w_x, w_y1)
                    state[state.index((b_x, b_y))] = (b_x, b_y + 1)  # Move pushed box left
                state.insert(0, (w_x, w_y1))
            elif action == 'Up':
                w_y1 = w_y - 1
                if (w_x, w_y1) in state:
                    (b_x, b_y) = (w_x, w_y1)
                    state[state.index((b_x, b_y))] = (b_x, b_y - 1)  # Move pushed box left
                state.insert(0, (w_x, w_y1))
        return tuple(state)

    def unpack_macro_action(self, node):
        """
        Returns a list of actions from a solution node of a ShortestPath problem
        :param node: solution node to a ShortestPath problem
        :return: list of actions or None
        """
        actions = []
        if node is None:
            return None
        else:
            path = node.path()
            for node in path:
                if node.action is not None:
                    actions.append(node.action)
            return actions

    def path_cost(self, c, state1, action, state2):
        """
        Calculates the path cost.
        If a macro action was used, the path cost is increased according to
        the number of actions given.
        If a single action is given it is simply the parent path cost + 1.

        :param c: parent path cost
        :param state1: parent state
        :param action: action(s) taken to state2
        :param state2: child state
        :return c: path cost from state1 to state2 by given action
        """
        if isinstance(action, list):
            return len(action) + c
        return c + 1

    def print_solution(self, goal_node):
        actions = []
        if goal_node is None:
            print "No solution found"
        elif goal_node == 'cuttoff':
            print "cuttoff"
        else:
            # path is list of nodes from initial state (root of the tree)
            path = goal_node.path()
            steps = 0
            print path[0].state
            print "to the goal state"
            print path[-1].state
            print "\nBelow is the sequence of moves\n"
            for node in path:
                if node.action is not None:
                    if isinstance(node.action, list):
                        for action in node.action:
                            steps += 1
                            print "{0}".format(action)
                            actions.append(action)
                    else:
                        print "{0}".format(node.action)
                        actions.append(node.action)
                        steps += 1
            print "Solution takes {0} steps from the initial state".format(steps)
            return actions


class ShortestPath(Problem):
    """
    Sub Problem class of the Sokoban puzzle
    Shortest path between a worker and a target location (macro action end point)
    """

    def __init__(self, worker, walls, boxes, target_location):
        """
        
        :param worker: 
        :param walls: 
        :param boxes: 
        :param target_location: 
        :return: 
        """
        self.initial = worker
        self.walls = walls
        self.boxes = boxes
        self.target_location = target_location


    def actions(self, state):
        """
        :param state: tuple of worker coords (w_x, w_y)
        :return actions: list of legal actions for the worker
        """

        actions = list()

        (w_x, w_y) = state  # get worker coords
        w_x_left = w_x - 1
        w_x_right = w_x + 1
        w_y_up = w_y - 1
        w_y_down = w_y + 1
        
        # check if left move is legal
        if (w_x_left, w_y) not in self.walls and (w_x_left, w_y) not in self.boxes:  # no walls and boxes
                actions.append('Left')
        if (w_x_right, w_y) not in self.walls and (w_x_right, w_y) not in self.boxes:
                actions.append('Right')
        if (w_x, w_y_down) not in self.walls and (w_x, w_y_down) not in self.boxes:
                actions.append('Down')
        if (w_x, w_y_up) not in self.walls and (w_x, w_y_up) not in self.boxes:
                actions.append('Up')
        return actions

    def result(self, state, action):
        """

        :param state:
        :param action:
        :return:
        """

        (w_x, w_y) = state
        if action == 'Left':
            return w_x - 1, w_y
        elif action == 'Right':
            return w_x + 1, w_y
        elif action == 'Up':
            return w_x, w_y - 1
        elif action == 'Down':
            return w_x, w_y + 1
        else:
            raise ValueError("Invalid action given")

    def goal_test(self, state):
        return state == self.target_location

    def h(self, node):
        """
        Manhattan distance
        :param node:
        :return:
        """
        (w_x, w_y) = node.state
        (t_x, t_y) = self.target_location
        dist = abs(w_x - t_x) + abs(w_y - t_y)
        return dist

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def checkActions(puzzleFileName, actionSequence):
        """
        This is a function called by the automatic marker.

        Your implementation should load a Sokoban puzzle from a text file,
        then try to apply the sequence of actions listed in actionSequence.

        @param puzzleFileName: file name of the puzzle
             (same format as for the files in the warehouses directory)
        @param actionSequence: a sequence of actions.
               For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
        @return:
            The string 'Failure', if one of the move was not successul.
               For example, if the agent tries to push two boxes,
                            or push into to push into a wall.
            Otherwise, if all moves were successful return                 
                   A string representing the state of the puzzle after applying
                   the sequence of actions.  This should be the same string as the
                   string returned by the method  WarehouseHowever.visualize()
        """

        soko = SokobanPuzzle(puzzleFileName)
        boxes = list(soko.warehouse.boxes)
        w_x, w_y = soko.warehouse.worker
        walls = soko.warehouse.walls

        for action in actionSequence:
            w_x0, w_y0 = w_x, w_y
            if action is "Left":
                # Check what is to the "Left"
                w_x1 = w_x0 - 1
                # check if wall is in the way
                if (w_x1, w_y0) in walls:
                    return "Failure"
                elif (w_x1, w_y0) in boxes:
                    s_x0, s_y0 = w_x1, w_y0
                    s_x1 = s_x0 - 1
                    if (s_x1, s_y0) in walls or (s_x1, s_y0) in boxes:
                        return "Failure"
                    else:
                        w_x = w_x1
                        boxes[boxes.index((s_x0, s_y0))] = (s_x1, s_y0)
                else:
                        w_x = w_x1
            elif action is "Right":
                # Check what is to the "Left"
                w_x1 = w_x0 + 1

                # check if wall is in the way
                if (w_x1, w_y0) in walls:
                    return "Failure"
                elif (w_x1, w_y0) in boxes:
                    s_x0, s_y0 = w_x1, w_y0
                    s_x1 = s_x0 + 1
                    if (s_x1, s_y0) in walls or (s_x1, s_y0) in boxes:
                        return "Failure"
                    else:
                        w_x = w_x1
                        boxes[boxes.index((s_x0, s_y0))] = (s_x1, s_y0)
                else:
                    w_x = w_x1

                # print soko.warehouse.visualize()
            elif action is "Down":
                # Check what is to the "Left"
                w_y1 = w_y0 + 1

                # check if wall is in the way
                if (w_x0, w_y1) in walls:
                    return "Failure"
                elif (w_x0, w_y1) in boxes:
                    s_x0, s_y0 = w_x0, w_y1
                    s_y1 = s_y0 + 1
                    if (s_x0, s_y1) in walls or (s_x0, s_y1) in boxes:
                        return "Failure"
                    else:
                        w_y = w_y1
                        boxes[boxes.index((s_x0, s_y0))] = (s_x0, s_y1)

                else:
                    w_y = w_y1


                # print soko.warehouse.visualize()
            elif action is "Up":
                w_y1 = w_y0 - 1
                if (w_x0, w_y1) in walls:
                    return "Failure"
                elif (w_x0, w_y1) in boxes:
                    s_x0, s_y0 = w_x0, w_y1
                    s_y1 = s_y0 - 1
                    if (s_x0, s_y1) in walls or (s_x0, s_y1) in boxes:
                        return "Failure"
                    else:
                        w_y = w_y1
                        boxes[boxes.index((s_x0, s_y0))] = (s_x0, s_y1)
                else:
                    w_y = w_y1
            else:
                raise ValueError("Invalid action given")
        soko.warehouse.worker = (w_x, w_y)
        soko.warehouse.boxes = boxes
        return soko.warehouse.visualize()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def tabooCells(puzzleFileName):
        """
        This is a function called by the automatic marker.

        Your implementation should load a Sokoban puzzle from a text file,
        then identify the cells that should be avoided in the sense that if
        a box get pushed on such a cell then the puzzle becomes unsolvable.

        @param puzzleFileName: file name of the puzzle
             (same format as for the files in the warehouses directory)
        @return:
                   A string representing the puzzle with the taboo cells marked with an 'X'.
                   Apart from the 'X's, the string should follows the same format as the
                   string returned by the method  Warehouse.visualize()
        """
        s = SokobanPuzzle(puzzleFileName)
        walls_y = [b for (a,b) in s.warehouse.walls]
        walls_x = [a for (a,b) in s.warehouse.walls]

        walls_x_start = min(walls_x)
        walls_x_end = max(walls_x)

        wall_y_start = min(walls_y)
        wall_y_end = max(walls_y)
        taboo = list()

        for row in xrange(wall_y_start + 1, wall_y_end):

            # get the walls above, below and on the current row
            row_above_walls = [a for (a,b) in s.warehouse.walls if b == row - 1]
            row_below_walls = [a for (a,b) in s.warehouse.walls if b == row + 1]
            row_current_walls = [a for (a,b) in s.warehouse.walls if b == row]

            # determine which pos can be accessed by boxes
            accessible_cells = list()

            # determine accessible warehouse positions (x position)
            for pos in xrange(row_current_walls[0],row_current_walls[-1] + 1):
                if pos not in row_current_walls:
                    if accessible_cells:  # not empty list
                        if (accessible_cells[-1] != '*') and ((pos - accessible_cells[-1]) != 1):
                            accessible_cells.append('*')
                        accessible_cells.append(pos)
                    else:
                        accessible_cells.append(pos)

            # process the accessible cells sub lists of continuous accessible cells
            accessible_segments = [[]]
            segment = 0

            for cell in accessible_cells:
                if cell == '*':
                    accessible_segments.append([])
                    segment += 1
                else:
                    accessible_segments[segment].append(cell)

            # check if any of the segments are empty, this is bad
            for segment in accessible_segments:
                if not segment:
                    raise ValueError("accessible segment is empty")

            # Begin determining taboo cells
            # Check if the cells are bounded by a U shape
            for segment in accessible_segments:
                bounded_upper_wall = True
                bounded_lower_wall = True
                target_in_segment = False  # Check if there is a target in segment
                for pos in segment:
                    if pos not in row_above_walls:
                        bounded_upper_wall = False
                    if pos not in row_below_walls:
                        bounded_lower_wall = False
                    if (pos, row) in s.warehouse.targets:  # target in segment, don't taboo it
                        target_in_segment = True

                if (bounded_upper_wall or bounded_lower_wall) and not target_in_segment:
                    for pos in segment:
                        taboo.append((pos, row))
                else:
                    for pos in segment:
                        if ((pos - 1) in row_current_walls or (pos + 1) in row_current_walls) and (pos in
                        row_below_walls or pos in row_above_walls):
                            taboo.append((pos, row))

        for col in xrange(walls_x_start + 1, walls_x_end):
            row_left_walls = [b for (a,b) in s.warehouse.walls if a == col - 1]
            row_right_walls = [b for (a,b) in s.warehouse.walls if a == col + 1]
            row_current_walls = [b for (a,b) in s.warehouse.walls if a == col]

            # determine which pos can be accessed by boxes
            accessible_cells = list()

            # determine accessible warehouse positions (y position)
            for pos in xrange(row_current_walls[0],row_current_walls[-1] + 1):
                if pos not in row_current_walls:
                    if accessible_cells:  # not empty list
                        if (accessible_cells[-1] != '*') and ((pos - accessible_cells[-1]) != 1):
                            accessible_cells.append('*')
                        accessible_cells.append(pos)
                    else:
                        accessible_cells.append(pos)

            # process the accessible cells sub lists of continuous accessible cells
            accessible_segments = [[]]
            segment = 0

            for cell in accessible_cells:
                if cell == '*':
                    accessible_segments.append([])
                    segment += 1
                else:
                    accessible_segments[segment].append(cell)

            # check if any of the segments are empty, this is bad
            for segment in accessible_segments:
                if not segment:
                    raise ValueError("accessible segment is empty")

             # Begin determining taboo cells
            # Check if the cells are bounded by a U shape
            for segment in accessible_segments:
                bounded_left_wall = True
                bounded_right_wall = True
                target_in_segment = False  # Check if there is a target in segment
                for pos in segment:
                    if pos not in row_left_walls:
                        bounded_left_wall = False
                    if pos not in row_right_walls:
                        bounded_right_wall = False
                    if (col, pos) in s.warehouse.targets:  # target in segment, don't taboo it
                        target_in_segment = True

                if (bounded_left_wall or bounded_right_wall) and not target_in_segment:
                    for pos in segment:
                        taboo.append((col, pos))
                else:
                    for pos in segment:
                        if ((pos - 1) in row_current_walls or (pos + 1) in row_current_walls) and (pos in
                        row_left_walls or pos in row_right_walls):
                            taboo.append((col, pos))


        def visualize_taboo_cells(walls, targets, boxes, taboo):
            X,Y = zip(*walls)  # pythonic version of the above
            x_size, y_size = 1+max(X), 1+max(Y)

            vis = [[" "] * x_size for y in range(y_size)]
            for (x,y) in walls:
                vis[y][x] = "#"
            for (x,y) in targets:
                vis[y][x] = "."
            for (x,y) in taboo:
                vis[y][x] = "X"
            return "\n".join(["".join(line) for line in vis])
        taboo_with_targets = [t for t in taboo if t not in s.warehouse.targets]

        return visualize_taboo_cells(s.warehouse.walls, s.warehouse.targets, s.warehouse.boxes, taboo_with_targets)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def solveSokoban_elementary(puzzleFileName, timeLimit = None):
        """
        This is a function called by the automatic marker.

        This function should solve the puzzle defined in a file.

        @param puzzleFileName: file name of the puzzle
             (same format as for the files in the warehouses directory)
        @param timeLimit: The time limit for this agent in seconds .
        @return:
            A list of strings.
            If timeout return  ['Timeout']
            If puzzle cannot be solved return ['Impossible']
            If a solution was found, return a list of elementary actions that solves
                the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
                For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
                If the puzzle is already in a goal state, simply return []
        """
        soko_problem = SokobanPuzzle(puzzleFileName)

        answer = astar_search(soko_problem)
        return answer


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def solveSokoban_macro(puzzleFileName, timeLimit = None):
        """
        This is a function called by the automatic marker.
        
        This function has the same purpose as 'solveSokoban_elementary', but 
        it should internally use macro actions as suggested 
        in the assignment description. Although it internally uses macro 
        actions, this function should return a sequence of 
        elementary  actions.


        @param puzzleFileName: file name of the puzzle
             (same format as for the files in the warehouses directory)
        @param timeLimit: The time limit for this agent in seconds .
        @return:
            A list of strings.
            If timeout return  ['Timeout']
            If puzzle cannot be solved return ['Impossible']
            If a solution was found, return a list elementary actions that solves
                the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
                For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
                If the puzzle is already in a goal state, simply return []
        """

        soko = SokobanPuzzleMacro(puzzleFileName)
        answer = astar_search(soko)
        return answer


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def test_solver(puzzleFileName):
    soko_problem = SokobanPuzzleMacro(puzzleFileName)
    answer = ida_star_search(soko_problem)
    return answer
