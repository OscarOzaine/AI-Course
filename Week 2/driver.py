import sys
import time
import psutil
import operator
from collections import deque

def display_board( state ):
	print "-------------"
	print "| %i | %i | %i |" % (state[0], state[1], state[2])
	print "-------------"
	print "| %i | %i | %i |" % (state[3], state[4], state[5])
	print "-------------"
	print "| %i | %i | %i |" % (state[6], state[7], state[8])
	print "-------------"
	
def move_up( state ):
	"""Moves the blank tile up on the board. Returns a new state as a list."""
	new_state = state[:]
	index = new_state.index( 0 )
	
	# Sanity check
	if index not in [0, 1, 2]:
		# Swap the values.
		temp = new_state[index - 3]
		new_state[index - 3] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None

def move_down( state ):
	"""Moves the blank tile down on the board. Returns a new state as a list."""
	new_state = state[:]
	index = new_state.index( 0 )
	# Sanity check
	if index not in [6, 7, 8]:
		# Swap the values.
		temp = new_state[index + 3]
		new_state[index + 3] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None

def move_left( state ):
	"""Moves the blank tile left on the board. Returns a new state as a list."""
	new_state = state[:]
	index = new_state.index( 0 )
	# Sanity check
	if index not in [0, 3, 6]:
		# Swap the values.
		temp = new_state[index - 1]
		new_state[index - 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None

def move_right(state):
	"""Moves the blank tile right on the board. Returns a new state as a list."""
	new_state = state[:]
	index = new_state.index( 0 )
	# Sanity check
	if index not in [2, 5, 8]:
		# Swap the values.
		temp = new_state[index + 1]
		new_state[index + 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None

def create_node(state, parent, operator, depth, cost):
	return Node(state, parent, operator, depth, cost)

def get_neighbor_value(state, move):
	value = 0
	if move == 'Up':
		move = 1
		value = move_up(state)
		
	elif move == 'Down':
		move = 2
		value = move_down(state)
		
	elif move == 'Left':
		move = 3
		value = move_left(state)
	elif move == 'Right':
		move = 4
		value = move_right(state)

	return_value = []
	return_value.append(move)

	if (value != None):
		return_value.append(state[value.index(0)])
	else:
		return_value.append(0)

	return return_value

def expand_node(parent_node):
	global count_expanded_nodes

	expanded_nodes = []
	expanded_nodes.append( create_node( move_up( parent_node.state ), parent_node, "Up", parent_node.depth + 1, 1 ) )
	expanded_nodes.append( create_node( move_down( parent_node.state ), parent_node, "Down", parent_node.depth + 1, 1 ) )
	expanded_nodes.append( create_node( move_left( parent_node.state ), parent_node, "Left", parent_node.depth + 1, 1 ) )
	expanded_nodes.append( create_node( move_right( parent_node.state), parent_node, "Right", parent_node.depth + 1, 1 ) )
	
	expanded_nodes = [node for node in expanded_nodes if node.state != None] #list comprehension!
	
	count_expanded_nodes += len(expanded_nodes)
	return expanded_nodes

def new_node(node, move):
	return_node = None
	if move == 1:
		return_node = create_node( move_up(node.state), node, "Up", node.depth + 1, 1 )
	elif move == 2:
		return_node = create_node( move_down(node.state), node, "Down", node.depth + 1, 1 )
	elif move == 3:
		return_node = create_node( move_left(node.state), node, "Left", node.depth + 1, 1 )
	elif move == 4:
		return_node = create_node( move_right(node.state), node, "Right", node.depth + 1, 1 )

	return return_node

def bfs(start, goal):

	global count_expanded_nodes

	nodes = []
	nodes.append(create_node(start, None, None, 0, 1))

	max_search_depth = 1
	max_fringe_size = 1
	while True:
		# We've run out of states, no solution.
		if len( nodes ) == 0: return None

		if max_fringe_size < len( nodes ):
			max_fringe_size = len( nodes )

		node = nodes.pop(0)

		if node.state == goal:
			path_to_goal = []
			temp = node
			search_depth = 0
			cost_of_path = 0

			while True:
				path_to_goal.insert(0, temp.operator)
				cost_of_path += temp.cost

				if temp.depth > search_depth:
					search_depth = temp.depth

				if temp.depth == 1: break
				temp = temp.parent

			return_value = {}
			return_value['path_to_goal'] = path_to_goal
			return_value['cost_of_path'] = cost_of_path
			return_value['nodes_expanded'] = count_expanded_nodes
			return_value['fringe_size'] = len( nodes ) + 1
			return_value['max_fringe_size'] = max_fringe_size
			return_value['search_depth'] = search_depth
			return_value['max_search_depth'] = max_search_depth

			return return_value

		if max_search_depth < len(nodes):
			max_search_depth = len(nodes)

		nodes.extend(expand_node(node))

def dfs(start, goal, depth = 20000):
	global count_expanded_nodes
	depth_limit = depth
	
	max_fringe_size = 0
	max_search_depth = 0

	frontier = Stack()
	frontier.push(create_node(start, None, None, 0, 1))
	visited = []
	count_expanded_nodes += 1

	while True:
		if frontier.size() == 0: return None

		if max_fringe_size < frontier.size():
			max_fringe_size = frontier.size()
		
		state = frontier.pop()

		visited.append(state.state.index(0))

		if state.state == goal:
			path_to_goal = []
			cost_of_path = 0
			search_depth = 0
			temp = state

			while True:
				path_to_goal.insert(0, temp.operator)
				cost_of_path += temp.cost

				if temp.depth > search_depth:
					search_depth = temp.depth
				
				if temp.depth <= 1: break
				temp = temp.parent

			return_value = {}
			return_value['path_to_goal'] = path_to_goal
			return_value['cost_of_path'] = cost_of_path

			return_value['len_visited'] = len(visited)
			return_value['nodes_expanded'] = count_expanded_nodes
			return_value['fringe_size'] = frontier.size() + 1
			return_value['max_fringe_size'] = max_fringe_size
			return_value['search_depth'] = search_depth
			return_value['max_search_depth'] = max_search_depth

			return return_value

		neighbors = state.create_neighbors(sort='asc')

		if neighbors != None:
			for neighbor in neighbors:

				if max_search_depth < neighbor.depth:
					max_search_depth = neighbor.depth

				if neighbor.state not in visited:
					frontier.push(neighbor)

	return None

class Node:
	def __init__(self, state, parent, operator, depth, cost):
		self.state = state
		self.parent = parent
		self.operator = operator
		self.depth = depth
		self.cost = cost
		self.neighbors = None

	def create_neighbors(self, sort='asc'):
		nodes = expand_node(self)

		if sort == 'asc':
			nodes = nodes
			nodes_dict = {}
			
			for n in nodes:
				nodes_dict[n.oldvalue()] = n

			nodes = sorted(nodes_dict.iteritems(), key=lambda (v,k): (v,k))
			nodes_dict = []
			for key, value in nodes:
				nodes_dict.append(value)

			nodes = nodes_dict
		else:
			nodes = nodes

		return nodes

	def neighbors(self):

		if self.neighbors == None:
			self.neighbors = expand_node(self)

		return self.neighbors

	def sorted_neighbors(self):
		neighbors = self.neighbors
		print "neighbors"
		print neighbors
		sys.exit()

	def oldvalue(self):
		return self.state[self.parent.state.index(0)]

def getParentKey(nodes):
	return nodes.oldvalue()

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop(0)

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def getItems(self):
    	nodes = self.items

    	states = []
    	for node in nodes:
    		states.append(node.state)

    	return states

count_expanded_nodes = 0

def main():
	global count_expanded_nodes
	start_time = time.time()

	goal_state = [0,1,2,3,4,5,6,7,8]

	method = sys.argv[1]
	board = list(sys.argv[2].split(','))
	board = map(int, board)
	starting_state = board

	result = None
	if method == 'bfs':
		result = bfs(starting_state, goal_state)
	elif method == 'dfs':
		result = dfs(starting_state, goal_state)

	if result == None:
		print "No solution found"
	elif result == [None]:
		print "Start node was the goal!"
	else:
		# Open a file
		fo = open("output.txt", "wb")
		fo.write("path_to_goal: " + str(result['path_to_goal']) + "\n");
		fo.write("cost_of_path: " + str(result['cost_of_path']) + "\n");
		fo.write("nodes_expanded: " + str(result['nodes_expanded']) + "\n");
		fo.write("fringe_size: " + str(result['fringe_size']) + "\n");
		fo.write("max_fringe_size: " + str(result['max_fringe_size']) + "\n");
		fo.write("search_depth: " + str(result['search_depth']) + "\n");
		fo.write("max_search_depth: " + str(result['max_search_depth']) + "\n");
		fo.write("running_time: " + str(time.time() - start_time) + "\n");
		fo.write("max_ram_usage: \n");

		# Close opend file
		fo.close()
		
		print result

if __name__ == "__main__":
	main()