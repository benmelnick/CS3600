# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    statesToVisit = util.Stack()  # the 'open' data structure
    visited = set()  # the 'closed' data structure
    pathMetadata = []  # metadata assigned to every state to track the path of how we got there - starts empty
    currState, currPath = (problem.getStartState(), pathMetadata)

    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.add(currState)
            for successor in problem.getSuccessors(currState):
                # successors are tuples w/ the following info: (state, direction from predecessor node, cost )
                # add successor to our stack
                statesToVisit.push((successor[0], currPath + [successor[1]]))
        currState, currPath = statesToVisit.pop()

    return currPath

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    pathMetadata = []
    statesToVisit = util.Queue()
    visited = set()
    currState, currPath = (problem.getStartState(), pathMetadata)

    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.add(currState)
            for successor in problem.getSuccessors(currState):
                statesToVisit.push((successor[0], currPath + [successor[1]]))
        currState, currPath = statesToVisit.pop()

    return currPath

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    statesToVisit = util.PriorityQueue()
    visited = set()
    pathMetadata = []
    gInit = 0
    currState, currPath, currG = (problem.getStartState(), pathMetadata, gInit)

    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.add(currState)
            for successor in problem.getSuccessors(currState):
                # send the priority along with state and metadata
                # priority is the total cost of getting to that exact node
                g = currG + successor[2]
                priority = g
                statesToVisit.push((successor[0], currPath + [successor[1]], g), priority)
        currState, currPath, currG = statesToVisit.pop()

    return currPath

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    statesToVisit = util.PriorityQueue()
    visited = set()
    pathMetadata = []
    gInit = 0
    currState, currPath, currG = (problem.getStartState(), pathMetadata, gInit)

    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.add(currState)
            for successor in problem.getSuccessors(currState):
                g = currG + successor[2]
                h = heuristic(successor[0], problem)
                priority = g + h
                # send just g in state tuple so h of the state doesn't affect g calculated in the future
                statesToVisit.push((successor[0], currPath + [successor[1]], g), priority)
        currState, currPath, currG = statesToVisit.pop()

    return currPath


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
