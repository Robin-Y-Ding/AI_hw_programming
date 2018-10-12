"""
COMS W4701 Artificial Intelligence - Programming Homework 1

In this assignment you will implement and compare different search strategies
for solving the n-Puzzle, which is a generalization of the 8 and 15 puzzle to
squares of arbitrary size (we will only test it with 8-puzzles for now).
See Courseworks for detailed instructions.

@author: Yangruibo Ding (yd2447)
"""

import time


def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped.
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]

    new_state = []
    for row in range(len(state)):
        new_row = []
        for column in range(len(state[row])):
            if row == i1 and column == j1:
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else:
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)


def move_left(child_states, state, h):
    new_ele = ["Left", swap_cells(state, h[0], h[1], h[0], h[1] + 1)]
    child_states.append(tuple(new_ele))
    return child_states


def move_right(child_states, state, h):
    new_ele = ["Right", swap_cells(state, h[0], h[1], h[0], h[1] - 1)]
    child_states.append(tuple(new_ele))
    return child_states


def move_up(child_states, state, h):
    new_ele = ["Up", swap_cells(state, h[0], h[1], h[0] + 1, h[1])]
    child_states.append(tuple(new_ele))
    return child_states


def move_down(child_states, state, h):
    new_ele = ["Down", swap_cells(state, h[0], h[1], h[0] - 1, h[1])]
    child_states.append(tuple(new_ele))
    return child_states


def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions.
    The result should be a list containing (Action, state) tuples.
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))),
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))]
    """

    child_states = []

    for i in range(0, len(state)):
        if 0 in state[i]:
            h2 = state[i].index(0)
            h = [i, h2]

    if h[0] == 0 or h[0] == len(state) - 1:
        if h[0] == 0:
            child_states = move_up(child_states, state, h)
        elif h[0] == len(state) - 1:
            child_states = move_down(child_states, state, h)
        if h[1] == 0:
            child_states = move_left(child_states, state, h)
        elif h[1] == len(state) - 1:
            child_states = move_right(child_states, state, h)
        else:
            child_states = move_left(child_states, state, h)
            child_states = move_right(child_states, state, h)
    elif h[1] == 0:
        child_states = move_left(child_states, state, h)
        child_states = move_up(child_states, state, h)
        child_states = move_down(child_states, state, h)
    elif h[1] == len(state) - 1:
        child_states = move_right(child_states, state, h)
        child_states = move_up(child_states, state, h)
        child_states = move_down(child_states, state, h)
    else:
        child_states = move_left(child_states, state, h)
        child_states = move_right(child_states, state, h)
        child_states = move_up(child_states, state, h)
        child_states = move_down(child_states, state, h)

    return child_states


def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise.
    """

    temp = []
    for i in range(0, len(state)):
        row = ()
        for j in range(0, len(state)):
            begin = i * len(state)
            row = row + ((begin + j),)
        temp.append(row)
    standard = tuple(temp)
    return state == standard


def bfs(state):  # still 10 more states
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a queue in BFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}
    state_format = ['None', state]  # to keep the format the same between the root node and its successors

    fringe.append(tuple(state_format))
    parents[tuple(state_format)] = []
    max_fringe += 1

    while(len(fringe) != 0):
        current = fringe.pop(0)
        if current[1] in closed:
            continue
        states_expanded += 1
        closed.add(current[1])
        if goal_test(current[1]):
            # Debugging: print parents[current]
            solution = []
            for tup in parents[current]:
                if tup[0] == 'None':
                    continue
                solution.append(tup[0])
            solution.append(current[0])
            return solution, states_expanded, max_fringe
        else:
            successors = get_successors(current[1])
            for successor in successors:
                if successor[1] in closed:
                    continue
                fringe.append(successor)
                parents.update({successor: (parents[current], current)})
                if len(fringe) > max_fringe:
                    max_fringe = len(fringe)

    #  return solution, states_expanded, max_fringe
    return None, states_expanded, max_fringe  # No solution found


def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a stack in DFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}

    state_format = ['None', state]

    fringe.append(tuple(state_format))
    parents[tuple(state_format)] = []
    max_fringe += 1

    while (len(fringe) != 0):
        current = fringe.pop()
        if current[1] in closed:
            continue
        states_expanded += 1
        closed.add(current[1])
        if goal_test(current[1]):
            # Debugging: print parents[current]
            solution = []
            for tup in parents[current]:
                if tup[0] == 'None':
                    continue
                solution.append(tup[0])
            solution.append(current[0])
            return solution, states_expanded, max_fringe
        else:
            successors = get_successors(current[1])
            for successor in successors:
                if successor[1] in closed:
                    continue
                fringe.append(successor)
                temp = list(parents[current])
                temp.append(current)
                parents[successor] = temp
                if len(fringe) > max_fringe:
                    max_fringe = len(fringe)

    #  return solution, states_expanded, max_fringe
    return None, states_expanded, max_fringe  # No solution found


def misplaced_heuristic(state):
    """
    Returns the number of misplaced tiles.
    """
    count = 0
    for i in range(0, len(state)):
        for j in range(0, len(state)):
            if (state[i][j] % (len(state)) != j) or (int(state[i][j] / (len(state))) != i):
                count += 1
    return count


def manhattan_heuristic(state):
    """
    For each misplaced tile, compute the Manhattan distance between the current
    position and the goal position. Then return the sum of all distances.
    """
    manhattan_sum = 0
    for i in range(0, len(state)):
        for j in range(0, len(state)):
            i0 = int(state[i][j] / (len(state)))
            j0 = state[i][j] % (len(state))
            manhattan_distance = abs(i - i0) + abs(j - j0)
            manhattan_sum += manhattan_distance
    return manhattan_sum  # replace this


def best_first(state, heuristic):
    """
    Best first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}
    state_format = ['None', state]  # to keep the format the same between the root node and its successors

    # fringe.append(tuple(state_format))
    heappush(fringe, (heuristic(state), tuple(state_format)))
    parents[tuple(state_format)] = []
    max_fringe += 1

    while (len(fringe) != 0):
        # current = fringe.pop(0)
        current = heappop(fringe)[1]
        if current[1] in closed:
            continue
        states_expanded += 1
        closed.add(current[1])
        if goal_test(current[1]):
            # Debugging: print parents[current]
            solution = []
            for tup in parents[current]:
                if tup[0] == 'None':
                    continue
                solution.append(tup[0])
            solution.append(current[0])
            return solution, states_expanded, max_fringe
        else:
            successors = get_successors(current[1])
            for successor in successors:
                if successor[1] in closed:
                    continue
                heappush(fringe, (heuristic(successor[1]), successor))
                temp = list(parents[current])
                temp.append(current)
                parents[successor] = temp
                if len(fringe) > max_fringe:
                    max_fringe = len(fringe)

    return None, states_expanded, max_fringe  # No solution found


def astar(state, heuristic):
    """
    A-star search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}
    costs = {}
    state_format = ['None', state]  # to keep the format the same between the root node and its successors

    # fringe.append(tuple(state_format))
    costs[tuple(state_format)] = 0
    heappush(fringe, (heuristic(state) + 0, tuple(state_format)))
    parents[tuple(state_format)] = []
    max_fringe += 1

    while (len(fringe) != 0):
        # current = fringe.pop(0)
        current = heappop(fringe)[1]
        if current[1] in closed:
            continue
        states_expanded += 1
        closed.add(current[1])
        if goal_test(current[1]):
            # Debugging: print parents[current]
            solution = []
            for tup in parents[current]:
                if tup[0] == 'None':
                    continue
                solution.append(tup[0])
            solution.append(current[0])
            return solution, states_expanded, max_fringe
        else:
            successors = get_successors(current[1])
            for successor in successors:
                if successor[1] in closed:
                    continue
                costs[successor] = costs[current] + 1
                heappush(fringe, (heuristic(successor[1]) + costs[successor], successor))
                temp = list(parents[current])
                temp.append(current)
                parents[successor] = temp
                if len(fringe) > max_fringe:
                    max_fringe = len(fringe)

    return None, states_expanded, max_fringe  # No solution found


def print_result(solution, states_expanded, max_fringe):
    """
    Helper function to format test output.
    """
    if solution is None:
        print("No solution found.")
    else:
        print("Solution has {} actions.".format(len(solution)))
    print("Total states expanded: {}.".format(states_expanded))
    print("Max fringe size: {}.".format(max_fringe))


if __name__ == "__main__":

    # Easy test case
    test_state = ((1, 4, 2),
                  (0, 5, 8),
                  (3, 6, 7))

    # More difficult test case
    # test_state = ((7, 2, 4),
    #               (5, 0, 6),
    #               (8, 3, 1))

    # print(state_to_string(test_state))
    # print ''

    print("====BFS====")
    start = time.time()
    solution, states_expanded, max_fringe = bfs(test_state)  #
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end - start))

    print()
    print("====DFS====")
    start = time.time()
    solution, states_expanded, max_fringe = dfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print ''
    print("====Greedy Best-First (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = best_first(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Total Manhattan Distance Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, manhattan_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))
