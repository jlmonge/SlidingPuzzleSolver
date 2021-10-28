from collections import deque

# optimal solution: https://www.youtube.com/watch?v=o4ZDw9oFlP8
# 

class Problem:
    def __init__(self, initial_state):
        self.initial_state = initial_state # list of inital positions of men
        self.goal_state = [1,2,3,4,5,6,7,8,9,0,0,0,0] # list of goal positionso f men
    def goal_test(self, state): # returns True if current state is goal state, else False
        return state == self.goal_state

class Node:
    def __init__(self, state, parent=None):
        self.state = state # list of current positions of men
        self.parent = parent

def general_search(problem, QUEUEING_FUNCTION):
    nodes = deque([problem.initial_state])    # deque

    while True:
        if len(nodes) == 0:
            return "Failure"
        node = nodes.popleft() # popleft() for fifo; pop for lifo()
        if problem.goal_state(node.state):
            return node
        #nodes = QUEUEING_FUNCTION(nodes, EXPAND(node, problem.OPERATORS)) # for loop
        #moves: 

problem = Problem([0,2,3,4,5,6,7,8,9,1,0,0,0])
general_search(problem)
while True:
    y_n = input("Would you like to try again with a different initial state? (y/n) ")
    if y_n.lower() == 'y':
        initial_state = input('''Enter the new initial state, with each value
        separated by commas''').split(',')
        problem = Problem(initial_state)


'''
output of initial state should look like
      0   0   0
0 2 3 4 5 6 7 8 9 1
how?
print(f'      {state[10]}   {state[11]}   {state[12]}')
for i in state[:10]:
    print(i, end=' ')
'''