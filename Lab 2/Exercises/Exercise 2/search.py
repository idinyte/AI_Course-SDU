from importlib.resources import path


class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

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


def TREE_SEARCH():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_FIRST(fringe)
        if node.STATE in GOAL_STATES:
            return node.path()
        children = EXPAND(node, node.path())
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''


def EXPAND(node, path):
    successors = []
    children = successor_fn(node.STATE)
    history = HISTORY(node)
    for child in children:
        if child in history:  # making sure states doesn't repeat
            continue

        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
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
Successor function, mapping the nodes to its successors
'''


def successor_fn(state):  # Lookup list of successor states
    # successor_fn( ('A', 'Clean', 'Clean')) returns [('A', 'Clean', 'Clean'), ('B', 'Clean', 'Clean')]
    return STATE_SPACE[state]


def HISTORY(node):
    return [p.STATE for p in node.path()]  # returns node history path


INITIAL_STATE = ('A', 'Dirty', 'Dirty')
GOAL_STATES = [('A', 'Clean', 'Clean'), ('B', 'Clean', 'Clean')]
STATE_SPACE = {('A', 'Dirty', 'Dirty'): [('A', 'Clean', 'Dirty'), ('A', 'Dirty', 'Dirty'), ('B', 'Dirty', 'Dirty')],
               ('B', 'Dirty', 'Dirty'): [('B', 'Dirty', 'Clean'), ('A', 'Dirty', 'Dirty'), ('B', 'Dirty', 'Dirty')],
               ('B', 'Dirty', 'Clean'): [('B', 'Dirty', 'Clean'), ('A', 'Dirty', 'Clean')],
               ('A', 'Dirty', 'Clean'): [('A', 'Clean', 'Clean'), ('A', 'Dirty', 'Clean'), ('B', 'Dirty', 'Clean')],
               ('A', 'Clean', 'Dirty'): [('A', 'Clean', 'Dirty'), ('B', 'Clean', 'Dirty')],
               ('B', 'Clean', 'Dirty'): [('B', 'Clean', 'Clean'), ('A', 'Clean', 'Dirty'), ('B', 'Clean', 'Dirty')],
               ('A', 'Clean', 'Clean'): [('A', 'Clean', 'Clean'), ('B', 'Clean', 'Clean')],
               ('B', 'Clean', 'Clean'): [('B', 'Clean', 'Clean'), ('A', 'Clean', 'Clean')], }


'''
Run tree search and display the nodes in the path to goal node
'''


def run():
    path = TREE_SEARCH()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()
