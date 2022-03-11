from importlib.resources import path


class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0, cost=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth
        self.COST = cost

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)   # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)


'''
Search the tree for the goal state and return path from initial state to goal state
'''


def GREEDY_BEST_FIRST(heuristic = 0):
    fringe = []
    initial_node = Node(INITIAL_STATE_H1) if heuristic == 0 else Node(INITIAL_STATE_H2)
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_LOWEST_HEURISTIC(fringe)
        if node.STATE[0] in GOAL_STATES:
            return node.path()
        children = EXPAND(node, heuristic)
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))

def A_STAR(heuristic = 0, weight = 1):
    fringe = []
    initial_node = Node(INITIAL_STATE_H1) if heuristic == 0 else Node(INITIAL_STATE_H2)
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_LOWEST_FUNCTION(fringe, weight)
        if node.STATE[0] in GOAL_STATES:
            return node.path()
        children = EXPAND(node, heuristic)
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''


def EXPAND(node, heuristic):
    successors = []
    children = successor_fn(node.STATE, heuristic)
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        s.COST = node.COST + s.STATE[1] # for A*
        successors = INSERT(s, successors)
    return successors


'''
Insert node in to the queue (fringe).
'''


def INSERT(node, queue):
    queue.append(node)
    return queue


'''
Insert list of nodes into the fringe
'''


def INSERT_ALL(l, queue):
    return queue + l


'''
Removes and returns the first element from fringe
'''


def REMOVE_FIRST(queue):
    return queue.pop(0)

'''
Removes and returns the element with lowest heuristic value from fringe
'''

def REMOVE_LOWEST_HEURISTIC(queue):
    return queue.pop(queue.index(min(queue,key=lambda q: q.STATE[0][1])))

'''
Removes and returns the element with lowest estimated total cost from fringe
'''

def REMOVE_LOWEST_FUNCTION(queue, weight):
    return queue.pop(queue.index(min(queue,key=lambda q: weight*q.STATE[0][1] + q.COST)))


'''
Successor function, mapping the nodes to its successors
'''


def successor_fn(state, heuristic):  # Lookup list of successor states
    return STATE_SPACE_DISTANCE[state[0]] if heuristic == 0 else STATE_SPACE_ALPHABET[state[0]]


INITIAL_STATE_H1 = [('A', 6), 0]
INITIAL_STATE_H2 = [('A', ord('L') - ord('A')), 0]
GOAL_STATES = [('K', 0), ('L', 0)]
STATE_SPACE_DISTANCE = {('A', 6): [[('B', 5), 1], [('C', 5), 2], [('D', 2), 4]],
                       ('B', 5): [[('A', 6), 1], [('E', 4), 4], [('F', 5), 5]],
                       ('C', 5): [[('A', 6), 2], [('E', 4), 1]],
                       ('D', 2): [[('A', 6), 4], [('H', 1), 1], [('I', 2), 4], [('J', 1), 2]],
                       ('E', 4): [[('B', 5), 4], [('C', 5), 1], [('G', 4), 2], [('H', 1), 3]],
                       ('F', 5): [[('B', 5), 5], [('G', 4), 1]],
                       ('G', 4): [[('E', 4), 2], [('F', 5), 1], [('K', 0), 6]],
                       ('H', 1): [[('D', 2), 1], [('E', 4), 3], [('K', 0), 6], [('L', 0), 5]],
                       ('I', 2): [[('D', 2), 4], [('L', 0), 3]],
                       ('J', 1): [[('D', 2), 2]], 
                       ('K', 0): [[('G', 4), 6], [('H', 1), 6]],
                       ('L', 0): [[('H', 1), 5], [('I', 2), 3]]
                       }

STATE_SPACE_ALPHABET = {('A', ord('L') - ord('A')): [[('B', ord('L') - ord('B')), 1], [('C', ord('L') - ord('C')), 2], [('D', ord('L') - ord('D')), 4]],
                       ('B', ord('L') - ord('B')): [[('A', ord('L') - ord('A')), 1], [('E', ord('L') - ord('E')), 4], [('F', ord('L') - ord('F')), 5]],
                       ('C', ord('L') - ord('C')): [[('A', ord('L') - ord('A')), 2], [('E', ord('L') - ord('E')), 1]],
                       ('D', ord('L') - ord('D')): [[('A', ord('L') - ord('A')), 4], [('H', ord('L') - ord('H')), 1], [('I', ord('L') - ord('I')), 4], [('J', ord('L') - ord('J')), 2]],
                       ('E', ord('L') - ord('E')): [[('B', ord('L') - ord('B')), 4], [('C', ord('L') - ord('C')), 1], [('G', ord('L') - ord('G')), 2], [('H', ord('L') - ord('H')), 3]],
                       ('F', ord('L') - ord('F')): [[('B', ord('L') - ord('B')), 5], [('G', ord('L') - ord('G')), 1]],
                       ('G', ord('L') - ord('G')): [[('E', ord('L') - ord('E')), 2], [('F', ord('L') - ord('F')), 1], [('K', ord('L') - ord('K')), 6]],
                       ('H', ord('L') - ord('H')): [[('D', ord('L') - ord('D')), 1], [('E', ord('L') - ord('E')), 3], [('K', ord('L') - ord('K')), 6], [('L', ord('L') - ord('L')), 5]],
                       ('I', ord('L') - ord('I')): [[('D', ord('L') - ord('D')), 4], [('L', ord('L') - ord('L')), 3]],
                       ('J', ord('L') - ord('J')): [[('D', ord('L') - ord('D')), 2]], 
                       ('K', ord('L') - ord('K')): [[('G', ord('L') - ord('G')), 6], [('H', ord('L') - ord('H')), 6]],
                       ('L', ord('L') - ord('L')): [[('H', ord('L') - ord('H')), 5], [('I', ord('L') - ord('I')), 3]]
                       }

'''
Run tree search and display the nodes in the path to goal node
'''


def run():
    print("\n\n Greedy best first")
    path = GREEDY_BEST_FIRST()
    print("\nSolution path:")
    for node in path:
        node.display()

    print("\n\n A* heuristic = default")
    path = A_STAR()
    print("\nSolution path:")
    for node in path:
        node.display()

    print("\n\n A* heuristic = distance between letters in alphabet. Heuristic is not admissible, so the solution is not optimal")
    path = A_STAR(1, 0.9)
    print("\nSolution path:")
    for node in path:
        node.display()

    print("\n\n 2 Times weighted A*, heuristic = default")
    path = A_STAR(0, 2) # Weighted A* with the weight of 2
    print("\nSolution path:")
    for node in path:
        node.display()
    
    print("\n\n 0.8 times weighted A*. Heuristic = distance between letters in alphabet. Heuristic weighted down to be admissible")
    path = A_STAR(1, 0.8) # Weighted A* with the weight of 2
    print("\nSolution path:")
    for node in path:
        node.display()

    print("\n\nConclusion: A* is much slower than greedy best first, but the solution is optimal.\nWeighted A* is a lot faster than A*, but slower than greedy best first and solution can be not optimal.\nGreedy best first is fastest, but solution is not optimal and can get stuck in loops.")


if __name__ == '__main__':
    run()
