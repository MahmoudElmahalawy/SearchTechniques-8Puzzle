### Student Info

# Assignment 1: 8 Puzzle.
#
### Language
# This assignment was written in Python. An open source, interpreted language
# with a mix of imperative, OO and functional programming. Syntax is simple
# and easy to learn.
#
# Developed on Ubuntu Linux but this will run on the interpreter available
# from http://python.org. Documentation is also on that site but a good
# tutorial is available for free at http://diveintopython.org.
#
### Data Structures
#
# The state of the board is stored in a list. The list stores values for the
# board in the following positions:
#
# -------------
# | 0 | 3 | 6 |
# -------------
# | 1 | 4 | 7 |
# -------------
# | 2 | 5 | 8 |
# -------------
#
# The goal is defined as:
#
# -------------
# | 1 | 2 | 3 |
# -------------
# | 8 | 0 | 4 |
# -------------
# | 7 | 6 | 5 |
# -------------
#
# Where 0 denotes the blank tile or space.
goal_state = [1, 8, 7, 2, 0, 6, 3, 4, 5]
#
# The code will read state from a file called "state.txt" where the format is
# as above but space seperated. i.e. the content for the goal state would be
# 1 8 7 2 0 6 3 4 5

### Code begins.


def display_board(state):
    print("-------------")
    print("| %i | %i | %i |" % (state[0], state[3], state[6]))
    print("-------------")
    print("| %i | %i | %i |" % (state[1], state[4], state[7]))
    print("-------------")
    print("| %i | %i | %i |" % (state[2], state[5], state[8]))
    print("-------------")


def move_up(state):
    """Moves the blank tile up on the board. Returns a new state as a list."""
    # Perform an object copy
    new_state = state[:]
    index = new_state.index(0)
    # Sanity check
    if index not in [0, 3, 6]:
        # Swap the values.
        temp = new_state[index - 1]
        new_state[index - 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        # Can't move, return None (Pythons NULL)
        return None


def move_down(state):
    """Moves the blank tile down on the board. Returns a new state as a list."""
    # Perform object copy
    new_state = state[:]
    index = new_state.index(0)
    # Sanity check
    if index not in [2, 5, 8]:
        # Swap the values.
        temp = new_state[index + 1]
        new_state[index + 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        # Can't move, return None.
        return None


def move_left(state):
    """Moves the blank tile left on the board. Returns a new state as a list."""
    new_state = state[:]
    index = new_state.index(0)
    # Sanity check
    if index not in [0, 1, 2]:
        # Swap the values.
        temp = new_state[index - 3]
        new_state[index - 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        # Can't move it, return None
        return None


def move_right(state):
    """Moves the blank tile right on the board. Returns a new state as a list."""
    # Performs an object copy. Python passes by reference.
    new_state = state[:]
    index = new_state.index(0)
    # Sanity check
    if index not in [6, 7, 8]:
        # Swap the values.
        temp = new_state[index + 3]
        new_state[index + 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        # Can't move, return None
        return None


def create_node(state, parent, operator, depth, cost):
    return Node(state, parent, operator, depth, cost)


def expand_node(node):
    """Returns a list of expanded nodes"""
    expanded_nodes = []
    expanded_nodes.append(create_node(move_up(node.state), node, "u", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_down(node.state), node, "d", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_left(node.state), node, "l", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_right(node.state), node, "r", node.depth + 1, 0))
    # Filter the list and remove the nodes that are impossible (move function returned None)
    expanded_nodes = [node for node in expanded_nodes if node.state != None]  # list comprehension!
    return expanded_nodes


def bfs(start, goal):
    """Performs a breadth first search from the start state to the goal"""
    # A list (can act as a queue) for the nodes.
    nodes = [create_node(start, None, None, 0, 0)]

    while True:
        current_node = nodes.pop(0)
        if current_node.state == goal:
            op = [current_node.operator]
            while current_node.parent:
                current_node = current_node.parent
                op.insert(0, current_node.operator)
            break
        else:
            nodes.extend(expand_node(current_node))
    return op


def dfs(start, goal, depth=10):
    """Performs a depth first search from the start state to the goal. Depth param is optional."""

    nodes = [create_node(start, None, None, 0, 0)]

    while True:
        current_node = nodes.pop(0)
        if current_node.state == goal:
            op = [current_node.operator]
            while current_node.parent:
                current_node = current_node.parent
                op.insert(0, current_node.operator)
            break
        elif current_node.depth <= depth:
            nodes = expand_node(current_node) + nodes
    return op


def ucs(start, goal):
    """Perfoms a uniform cost search from the start state to the goal."""
    
    nodes = [create_node(start, None, None, 0, 0)]
    
    while True:
        cost_list = [nodes[i].depth for i in range(len(nodes))]
        min_cost = min(cost_list)
        min_index = cost_list.index(min_cost)
        current_node = nodes.pop(min_index)

        if current_node.state == goal:
            op = [current_node.operator]
            while current_node.parent:
                current_node = current_node.parent
                op.insert(0, current_node.operator)
            break
        else:
            nodes = nodes[:min_index] + expand_node(current_node) + nodes[min_index:]
    return op


def ids(start, goal, depth=50):
	"""Perfoms an iterative depth first search from the start state to the goal. Depth is optional."""
	for i in range( depth ):
		result = dfs( start, goal, i )
		if result != None:
			return result






# Node data structure
class Node:
    def __init__(self, state, parent, operator, depth, cost):
        # Contains the state of the node
        self.state = state
        # Contains the node that generated this node
        self.parent = parent
        # Contains the operation that generated this node from the parent
        self.operator = operator
        # Contains the depth of this node (parent.depth +1)
        self.depth = depth
        # Contains the path cost of this node from depth 0. Not used for depth/breadth first.
        self.cost = cost


def readfile(filename):
    f = open(filename)
    data = f.read()
    # Get rid of the newlines
    data = data.strip("\n")
    # Break the string into a list using a space as a seperator.
    data = data.split(" ")
    state = []
    for element in data:
        state.append(int(element))
    return state


# Main method
def main():
    starting_state = readfile("state.txt")
    ### CHANGE THIS FUNCTION TO USE bfs, dfs, ids or a_star
    result = ucs(starting_state, goal_state)
    
    if result == None:
        print("No solution found")
    elif result == [None]:
        print("Start node was the goal!")
    else:
        result.remove(None)
        print(result)
        print(len(result), " moves")


# A python-isim. Basically if the file is being run execute the main() function.
if __name__ == "__main__":
    main()
