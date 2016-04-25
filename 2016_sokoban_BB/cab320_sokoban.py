import operator

"""
Code for a CAB320 assignment
Last modified 2016-03-22
by f.maire@qut.edu.au
"""

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           UTILS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def findIterator(haystack, needle):
    """
    Return a generator that yield the positions (offset indices)
       where the character 'needle' appears in the  'haystack' string.
    :param haystack: a string where we might find occurrences of the 'needle' character.
    :param needle: a character that we are looking for.
    :return: iterator
    """
    pos = 0
    pos = haystack.find(needle, pos)
    while pos != -1:
        yield pos
        pos = haystack.find(needle, pos+1)


def findPositionIterator(lines, char):
    """
    Return a generator that  yields the (x,y) positions of
        the occurrences of the character 'char' in the list of string 'lines'.
        A tuple (x,y) is returned, where
        x is the horizontal coord (column offset),
        and  y is the vertical coord (row offset)
    :param lines: a list of strings
    :param char: character of interest
    :return: tuple of x and y coords
    """
    for y, line in enumerate(lines):
        for x in findIterator(line, char):
            yield (x,y)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Warehouse:
    """
    A Warehouse object represents the configuration of a warehouse, including
    the position of the walls, targets, boxes and the worker.
    Self.boxes, self.targets and self.walls  are lists of (x,y) coordinates
    self.worker is a tuple (x,y)

    self.worker
    """

    def copy(self, worker = None, boxes = None):
        """
        Make a copy of this warehouse. Possibly with new positions
        for the worker and the boxes.  Targets and Walls are copied (shallow copy)
        worker : a (x,y) tuple, position of the agent
        boxes : list of (x,y) pairs, positions of the boxes
        """
        result = Warehouse()
        result.worker = worker or self.worker
        result.boxes = boxes or self.boxes
        result.targets = self.targets
        result.walls = self.walls
        return result

    def read_warehouse_file(self, filePath):
        """
        Load the description of a warehouse stored in a text file
        :param filePath
        """
        with open(filePath, 'r') as f:
            # 'lines' is a list of strings (rows of the puzzle) 
            lines = f.readlines()
        self.extract_locations(lines)
    
    def write_warehouse_file(self, filePath):
        with open(filePath, 'w') as f:
            f.write(self.visualize())

    def extract_locations(self, lines):
        """
        Extract positional information from the string
        representation of the puzzle.
        """
        workers = list(findPositionIterator(lines, "@"))  # workers on a free cell
        workers_on_a_target = list(findPositionIterator(lines, "!"))
        # Check that we have exactly one agent
        assert len(workers)+len(workers_on_a_target) == 1 
        if len(workers) == 1:
            self.worker = workers[0]
        self.boxes = list(findPositionIterator(lines, "$")) # crate/box
        self.targets = list(findPositionIterator(lines, ".")) # empty target
        targets_with_boxes = list(findPositionIterator(lines, "*")) # box on target
        self.boxes += targets_with_boxes
        self.targets += targets_with_boxes
        if len(workers_on_a_target) == 1:
            self.worker = workers_on_a_target[0]
            self.targets.append(self.worker) 
        self.walls = list(findPositionIterator(lines, "#")) # set(findPositionIterator(lines, "#"))
        assert len(self.boxes) == len(self.targets)

    def visualize(self):
        """
        Return a string representation of the warehouse
        """
        ##        x_size = 1+max(x for x,y in self.walls)
        ##        y_size = 1+max(y for x,y in self.walls)
        X,Y = zip(*self.walls) # pythonic version of the above
        x_size, y_size = 1+max(X), 1+max(Y)
        
        vis = [[" "] * x_size for y in range(y_size)]
        for (x,y) in self.walls:
            vis[y][x] = "#"
        for (x,y) in self.targets:
            vis[y][x] = "."
        # if worker is on a target display a "!", otherwise a "@"
        # exploit the fact that Targets has been already processed
        if vis[self.worker[1]][self.worker[0]] == ".": # Note y is worker[1], x is worker[0]
            vis[self.worker[1]][self.worker[0]] = "!"
        else:
            vis[self.worker[1]][self.worker[0]] = "@"
        # if a box is on a target display a "*"
        # exploit the fact that Targets has been already processed
        for (x,y) in self.boxes:
            if vis[y][x] == ".": # if on target
                vis[y][x] = "*"
            else:
                vis[y][x] = "$"
        return "\n".join(["".join(line) for line in vis])



    def __eq__(self, other):
        return self.worker == other.worker and \
               self.boxes == other.boxes

    def __hash__(self):
        return hash(self.worker) ^ reduce(operator.xor, [hash(box) for box in self.boxes])

    """
    Movement of worker
    """
    def moveUp(self):
        x, y = self.worker
        new_x, new_y = x, y-1
        self.worker = (new_x, new_y)

    def moveDown(self):
        x, y = self.worker
        new_x, new_y = x, y+1
        self.worker = (new_x, new_y)

    def moveRight(self):
        x, y = self.worker
        new_x, new_y = x+1, y
        self.worker = (new_x, new_y)

    def moveLeft(self):
        x, y = self.worker
        new_x, new_y = x-1, y
        self.worker = (new_x, new_y)

    """
    Movement of boxes
    """
    def pushBoxUp(self, x, y):
        try:
            boxIndex = self.boxes.index((x,y))
            x,y = self.boxes[boxIndex]
            y -= 1
            self.boxes[boxIndex] = (x,y)
            return True
        except ValueError:
            return False

    def pushBoxDown(self, x, y):
        try:
            boxIndex = self.boxes.index((x,y))
            x,y = self.boxes[boxIndex]
            y += 1
            self.boxes[boxIndex] = (x,y)
            return True
        except ValueError:
            return False

    def pushBoxLeft(self, x, y):
        try:
            boxIndex = self.boxes.index((x,y))
            x,y = self.boxes[boxIndex]
            x -= 1
            self.boxes[boxIndex] = (x,y)
            return True
        except ValueError:
            return False

    def pushBoxRight(self, x, y):
        try:
            boxIndex = self.boxes.index((x,y))
            x,y = self.boxes[boxIndex]
            x += 1
            self.boxes[boxIndex] = (x,y)
            return True
        except ValueError:
            return False
    
# if __name__ == "__main__":
    
    # field = Warehouse()
    # field.read_warehouse_file("./warehouses/warehouse_01.txt")
    # field.write_warehouse_file("./F_01.txt")

    # print field.visualize()


# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +
#                              CODE CEMETERY
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +


#     """
#     Actions available are Up, Down, Left and Right.
#     """
#     def actions(self):
#         actions = list()
#         w_x0, w_y0 = self.worker
#
#         w_x_left = w_x0 - 1
#         w_x_right = w_x0 + 1
#         w_y_down = w_y0 + 1
#         w_y_up = w_y0 - 1
#
#         if (w_x_left, w_y0) not in self.walls:
#             if(w_x_left, w_y0) not in self.boxes:
#                 actions.append('Left')
#             else:
#                 # theres a box there, check if theres no box & wall to the new box pos
#                 b_x0 = w_x_left - 1
#                 b_y0 = w_y0
#                 if (b_x0, b_y0) not in self.walls and (b_x0, b_y0) not in self.boxes:
#                     actions.append('Left')
#
#         # check right
#         if (w_x_right, w_y0) not in self.walls:
#             if(w_x_right, w_y0) not in self.boxes:
#                 actions.append('Right')
#             else:
#                 # theres a box there, check if theres no box & wall to the new box pos
#                 b_x0 = w_x_right + 1
#                 b_y0 = w_y0
#                 if (b_x0, b_y0) not in self.walls and (b_x0, b_y0) not in self.boxes:
#                     actions.append('Right')
#
#         # check up
#         if (w_x0, w_y_up) not in self.walls:
#             if(w_x0, w_y_up) not in self.boxes:
#                 actions.append('Up')
#             else:
#                 # theres a box there, check if theres no box & wall to the new box pos
#                 b_x0 = w_x0
#                 b_y0 = w_y0 - 1
#                 if (b_x0, b_y0) not in self.walls and (b_x0, b_y0) not in self.boxes:
#                     actions.append('up')
#
#         # check down
#         if (w_x0, w_y_down) not in self.walls:
#             if(w_x0, w_y_down) not in self.boxes:
#                 actions.append('Down')
#             else:
#                 # theres a box there, check if theres no box & wall to the new box pos
#                 b_x0 = w_x0
#                 b_y0 = w_y0 + 1
#                 if (b_x0, b_y0) not in self.walls and (b_x0, b_y0) not in self.boxes:
#                     actions.append('Down')
#
#         return actions