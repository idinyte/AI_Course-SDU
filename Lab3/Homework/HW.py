from importlib.resources import path

class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, pos, parent=None, depth=0, cost=0):
        self.STATE = state
        self.POSITION = pos
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
        return 'State: ' + str(self.STATE) + ' - POSITION: ' + str(self.POSITION) + ' - MOVE: ' + str(self.DEPTH) + ' - COST: ' + str(self.COST)

def A_STAR():
    fringe = []
    initial_node = Node(Current_state, START_SQUARE)
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_LOWEST_FUNCTION(fringe)
        if node.STATE == GOAL_STATE:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))

'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''


def EXPAND(node):
    successors = []
    children = successor_fn(node)
    for child in children:
        s = Node(node, child)  # create node for each in state list
        s.STATE = node.STATE
        if child not in node.STATE: # if we cleaned the square, remove it from successors
          temp = node.STATE.copy()
          temp[temp.index([child[0], 'Dirty'])] = child
          s.STATE = temp
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        s.COST = node.COST + CALCULATE_MOVE_COST(child, node)
        successors = INSERT(s, successors)
    return successors

def CALCULATE_MOVE_COST(child, node):
  for i in MOVE_COST[node.POSITION[0]]:
    if i[0] == child[0]:
      return i[1]
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
Removes and returns the element with lowest estimated total cost from fringe
'''

def REMOVE_LOWEST_FUNCTION(queue):
  return queue.pop(queue.index(min(queue,key=lambda q: CALCULATE_HEURISTIC(q) + q.COST)))


'''
Calculates and return heuristic, which in this case is number of dirty squares
'''

def CALCULATE_HEURISTIC(node):
  return len(list(filter(lambda n: n[1] == 'Dirty' , node.STATE)))


'''
Successor function, mapping the nodes to its successors
'''

def successor_fn(node):  # Lookup list of successor states
  successor_list = []
  for n in node.STATE:
    if n[0] != node.POSITION[0]:
      successor_list.append(n)
    elif n[1] == 'Dirty':
      successor_list.append([n[0], 'Clean'])

  return successor_list


A = 'A'
B = 'B'
C = 'C'
D = 'D'

'''
Locations:

A | B
-----
C | D
'''

Current_state = [[A, 'Dirty'], [B, 'Clean'], [C, 'Dirty'], [D, 'Dirty']]
START_SQUARE = Current_state[0]
GOAL_STATE = [[A, 'Clean'], [B, 'Clean'], [C, 'Clean'], [D, 'Clean']]

MOVE_COST = {                         # Costs: 0 - clean own square, 1 - move to sides, 2 - move diagonaly
  A: [(A, 0), (B, 1), (C, 1), (D, 2)],
  B: [(A, 1), (B, 0), (C, 2), (D, 1)],
  C: [(A, 1), (B, 2), (C, 0), (D, 1)],
  D: [(A, 2), (B, 1), (C, 1), (D, 0)]
}

if __name__ == '__main__':
  path = A_STAR()
  print("\nSolution path:")
  for node in path:
      node.display()
