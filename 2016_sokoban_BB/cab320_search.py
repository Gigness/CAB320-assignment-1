#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This search module is based on the AIMA book.
Search (Chapters 3-4)

The way to use this code is to subclass Problem to create a class of problems,
then create problem instances and solve them with calls to the various search
functions.

Last modified 2016-03-12
by f.maire@qut.edu.au

Simplified code, and added further comments

"""

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           UTILS

import collections  # for dequeue
import heapq
import sys
import time


# Examine this function after completing "cab320/wk03/challenge 2"


def memoize(fn):
    """Memoize fn: make it remember the computed value for any argument list"""

    def memoized_fn(*args):
        if not memoized_fn.cache.has_key(args):
            memoized_fn.cache[args] = fn(*args)
        return memoized_fn.cache[args]

    memoized_fn.cache = {}
    return memoized_fn


def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


# ______________________________________________________________________________
# Queues: 
#       LIFOQueue: "Last In First Out", also known as stack
#       FIFOQueue: "First In First Out", standard queue 
#       PriorityQueue:  also known as heap

class Queue:
    """
    Queue is an abstract class/interface. There are three types:
        LIFOQueue(): A Last In First Out Queue.
        FIFOQueue(): A First In First Out Queue.
        PriorityQueue(f): Queue in sorted order (min f first).
    Each type of queue supports the following methods and functions:
        q.append(item)  -- add an item to the queue
        q.extend(items) -- equivalent to: for item in items: q.append(item)
        q.pop()         -- return the top item from the queue
        len(q)          -- number of items in q (also q.__len())
        item in q       -- does q contain item?
    """

    def __init__(self):
        raise NotImplementedError

    def extend(self, items):
        for item in items: self.append(item)


def LIFOQueue():
    """
    Return an empty list, suitable as a Last-In-First-Out Queue.
    Last-In-First-Out Queues are also called stacks
    """
    return []


class FIFOQueue(collections.deque):
    """
    A First-In-First-Out Queue.
    collections.deque where deque.popleft is renamed to "pop", just use a deque...
    """

    def __init__(self):
        collections.deque.__init__(self)

    def pop(self):
        return self.popleft()  # remove and return the elt at position 0


class PriorityQueue(Queue):
    """
    A queue in which the minimum  element (as determined by f) is returned first.
    The item with minimum f(x) is returned first
    """

    def __init__(self, f=lambda x: x):
        self.A = []
        self.f = f

    def append(self, item):
        heapq.heappush(self.A, (self.f(item), item))

    def __len__(self):
        return len(self.A)

    def __str__(self):
        return str(self.A)

    def pop(self):
        return heapq.heappop(self.A)[1]
        # (self.f(item), item) is returned by heappop
        # (self.f(item), item)[1]   is item

    def __contains__(self, item):
        # Note that on the next line a generator is used!
        return any(x == item for _, x in self.A)

    def __getitem__(self, key):
        for _, item in self.A:
            if item == key:
                return item
                # return None if item is not in the queue

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.A):
            if item == key:
                self.A.pop(i)
                heapq.heapify(self.A)
                return


# ______________________________________________________________________________


class Problem(object):
    """The abstract class for a formal problem.  You should subclass
    this class and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial;
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""

        return c + 1


# ______________________________________________________________________________

class Node:
    """
    A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class.
    """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """ Create a search tree Node, derived from a parent by an action."""
        update(self, state=state, parent=parent, action=action, path_cost=path_cost, depth=0)
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def expand(self, problem):
        "List the nodes reachable in one step from this node."
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        "Fig. 3.10"
        next = problem.result(self.state, action)

        child_node_path_cost = self.path_cost
        return Node(next,  # next is a state
                    self,  # parent is a node
                    action,  # from this state to next state
                    problem.path_cost(self.path_cost, self.state, action, next)
                    )

    def solution(self):
        "Return the sequence of actions to go from the root to this node."
        return [node.action for node in self.path()[1:]]

    def path(self):
        "Return a list of nodes forming the path from the root to this node."
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


# ______________________________________________________________________________

# Uninformed Search algorithms


def tree_search(problem, frontier):
    """
        Search through the successors of a problem to find a goal.
        The argument frontier should be an empty queue.
        Don't worry about repeated paths to a state. [Fig. 3.7]
        Return
             the node of the first goal state found
             or None is no goal state is found
    """
    assert isinstance(problem, Problem)

    node = Node(problem.initial)

    # Debug
    print node
    print dir(node)
    print node.state
    print type(node.state)
    # end Debug

    if problem.goal_test(node.state):
        return node
    frontier.append(node)

    while frontier:
        # print frontier
        currentNode = frontier.pop()
        # print "popped: ", currentNode
        if problem.goal_test(currentNode.state):
            return currentNode
        for childNode in currentNode.expand(problem):
            if childNode not in frontier:
                # print "push: ", childNode
                frontier.append(childNode)
    return None


def graph_search(problem, frontier):
    """
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    If two paths reach a state, only use the first one. [Fig. 3.7]
    Return
        the node of the first goal state found
        or None is no goal state is found
    """
    assert isinstance(problem, Problem)
    frontier.append(Node(problem.initial))
    explored = set()  # initial empty set of explored states
    while frontier:
        leafNode = frontier.pop()
        if problem.goal_test(leafNode.state):
            return leafNode
        explored.add(leafNode.state)
        # Python note: next line uses of a generator
        frontier.extend(child for child in leafNode.expand(problem)
                        if child.state not in explored
                        and child not in frontier)
    return None


def breadth_first_tree_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """

    frontier = FIFOQueue()
    frontier.append(Node(problem.initial))

    while frontier:
        currentNode = frontier.pop()
        if problem.goal_test(currentNode.state):
            return currentNode

        frontier.extend(child for child in currentNode.expand(problem) if child not in frontier)

    return None


def depth_first_tree_search(problem):
    "Search the deepest nodes in the search tree first."
    return tree_search(problem, LIFOQueue())


def depth_first_graph_search(problem):
    "Search the deepest nodes in the search tree first."
    return graph_search(problem, LIFOQueue())


def breadth_first_search(problem):
    "Graph search version.  [Fig. 3.11]"
    node = Node(problem.initial)
    frontier = FIFOQueue()
    frontier.append(node)
    explored = set()
    while frontier:
        currentNode = frontier.pop()
        explored.add(currentNode.state)
        if problem.goal_test(currentNode.state):
            return currentNode
        frontier.extend(
                child for child in currentNode.expand(problem) if child not in frontier and child.state not in explored)
    return None


def best_first_graph_search(problem, f):
    """
    Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned.
    """
    # set up cache-able function f
    f = memoize(f)

    node = Node(problem.initial)

    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(f)
    frontier.append(node)
    explored = set()
    while frontier:
        # print frontier
        node = frontier.pop()
        # print node

        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]  # incumbent is a node
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None


def best_first_graph_search_timeout(problem, f, timeLimit=None):
    """
    best_first_graph_search implemented with a timeout feature.
    Checks if the time limit is exceeded before a frontier node is expanded.
    """
    # set up cache-able function f
    t0 = time.time()
    f = memoize(f)

    node = Node(problem.initial)

    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(f)
    frontier.append(node)
    explored = set()
    while frontier:
        if (timeLimit is not None) and (time.time() - t0) > timeLimit:
            return 'timeout'
        node = frontier.pop()

        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]  # incumbent is a node
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None


def uniform_cost_search(problem):
    """[Fig. 3.14]"""
    return best_first_graph_search(problem, lambda node: node.path_cost)


def depth_limited_search(problem, limit=50):
    """[Fig. 3.17]"""

    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result

            if cutoff_occurred:
                return 'cutoff'
            else:
                return None

    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    """[Fig. 3.18]"""
    for depth in xrange(sys.maxint):

        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result

#______________________________________________________________________________
# Informed (Heuristic) Search

greedy_best_first_graph_search = best_first_graph_search
# Greedy best-first search is accomplished by specifying f(n) = h(n).


def astar_search_timeout(problem, h=None, timeLimit=None):
    """
    same as astar_search but with Timeout functionality
    """
    h = memoize(h or problem.h)
    return best_first_graph_search_timeout(problem, lambda n: n.path_cost + h(n), timeLimit=timeLimit)


def astar_search(problem, h=None):
    """A* search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h)
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def ida_star_search_elementary(problem):
    """
    ida* search implemented by increasing the depth bound by 1 each time.
    """
    for f_val in xrange(sys.maxint):
        result = a_star_limited_search(problem, f_val)
        if result != 'cutoff':
            return result


def a_star_limited_search(problem, f_val=50):
    """
    Elementary solve a star, where fbound is simply increased by 1
    """

    h = memoize(problem.h)
    f = (lambda node: node.path_cost + h(node))

    def recursive_a_star(node, problem, f_val):
        print "f(", node, ") ", f(node), " , f_val: ", f_val
        if problem.goal_test(node.state):
            return node
        elif f(node) >= f_val:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_a_star(child, problem, f_val)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result

            if cutoff_occurred:
                return 'cutoff'
            else:
                return None

    # Body of depth_limited_search:
    return recursive_a_star(Node(problem.initial), problem, f_val)


def ida_star_search(problem):
    """
    IDA* implemented from Wikipedia pseudo code.
    https://en.wikipedia.org/wiki/Iterative_deepening_A*

    :param problem:
    :return: solution node or None
    """

    def a_star_bounded_search(node, bound):
        """
        Recursive implementation of a depth bounded a* search

        :param node: initial node
        :param bound: limit of f(n) values
        :return: Node or new bound limit
        """

        # check the f value of the node
        f_val = f(node)

        # check if its a goal or if its f value exceeds the bound
        if problem.goal_test(node.state):
            return node
        elif f_val > bound:
            return f_val

        f_min = sys.maxint  # set the current f_min to infinity

        for child in node.expand(problem):
            t = a_star_bounded_search(child, bound)
            if isinstance(t, int):  # f bound surpassed
                if t < f_min:
                    f_min = t
            elif t is not None:  # found a goal
                return t

        return f_min

    h = memoize(problem.h)
    f = (lambda node: node.path_cost + h(node))

    root = Node(problem.initial)
    bound = f(root)

    while True:
        result = a_star_bounded_search(root, bound)
        if result == sys.maxint:  # no solution exists
            return None
        elif isinstance(result, int):
            bound = result  # cuttoff, set a new bound val
        else:
            return result


def ida_star_search_limited(problem, limit):
    """
    Test function to run ida* to a given depth bound.
    the depth bound is the f(n) value of a node.
    :param problem:
    :param limit:
    :return:
    """
    def a_star_bounded_search(node, bound):
        f_val = f(node)

        if f_val > bound:
            return f_val
        elif problem.goal_test(node.state):
            return node

        f_min = float('inf')

        for child in node.expand(problem):
            result = a_star_bounded_search(child, bound)
            if isinstance(result, int):  # f bound surpassed
                if result < f_min:
                    f_min = result
            elif result is not None:  # found a goal
                return result

        return f_min

    h = memoize(problem.h)
    f = (lambda node: node.path_cost + h(node))

    root = Node(problem.initial)
    bound = f(root)

    while bound < limit:

        result = a_star_bounded_search(root, bound)
        if result == float('inf'):  # no solution exists
            return None
        elif isinstance(result, int):
            bound = result
        else:
            return result


#______________________________________________________________________________
#

