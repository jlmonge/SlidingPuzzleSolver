from collections import deque

# optimal solution: https://www.youtube.com/watch?v=o4ZDw9oFlP8

'''
Moves used in optimal result:
1. go all the way left,
2. go all the way right, and
3. go up the closet available reccess.
This is fine; the instructions say that a man may go any distance
that is possible in a move, so I decided it would be best for the men
to move only in optimal moves, as used in the optimal solution. 
'''

class Problem:
    def __init__(self, initial_state):
        self.initial_state = initial_state # list of inital positions of men
        self.goal_state = [[0,0,0],[1,2,3,4,5,6,7,8,9,0]] # lists of goal positions of men
    def goal_test(self, state): # returns True if current state is goal state, else False
        return state == self.goal_state

class Node:
    def __init__(self, state, parent=None):
        self.state = state # list of current positions of men
        self.parent = parent

def general_search(problem, QUEUEING_FUNCTION):
    nodes = deque([problem.initial_state])    # deque

    while True:
        if len(nodes) == 0: # every node has been visited
            return "Failure"
        node = nodes.popleft() # popleft() for fifo; pop for lifo()
        if problem.goal_state(node.state): # 
            return node
        #nodes = QUEUEING_FUNCTION(nodes, EXPAND(node, problem.OPERATORS)) # for loop
        #moves: 

def user_input():
    print("Welcome to Nine Men in a Trench\n" +
        "      0   0   0\n" +
        "1 2 3 4 5 6 7 8 9 0\n" +
        "0: blank space\n" +
        "1: sergeant\n" +
        "2-9: other men in the trench\n" +
        "*** INSTRUCTIONS ***\n"
        "There must be 4 blank spaces, and each positive number " +
        "must be used once.")
    invalid_input = True
    while invalid_input:
        # split converts input to list
        first_row = input("Enter the first row (3 entries): ").split()
        second_row = input("Enter the second row (10 entries): ").split()

        if len(first_row) != 3 or len(second_row) != 10:
            continue

        num_blanks = 0
        positive_set = set()
        invalid_input = False
        for i in range(3):
            first_row[i] = int(first_row[i])
            if first_row[i] == 0 and num_blanks < 5:
                num_blanks += 1
            elif (first_row[i] > 0 and first_row[i] < 10 and 
                    first_row[i] not in positive_set):
                positive_set.add(first_row[i])
            else:
                invalid_input = True
        for i in range(10):
            second_row[i] = int(second_row[i])
            if second_row[i] == 0 and num_blanks < 5:
                num_blanks += 1
            elif (second_row[i] > 0 and second_row[i] < 10 and 
                    second_row[i] not in positive_set):
                positive_set.add(second_row[i])
            else:
                invalid_input = True
        
    user_puzzle = [first_row, second_row]
    return user_puzzle

def main():
    user_puzzle = user_input()
    problem = Problem(user_puzzle)
    #general_search(problem)
    #problem = Problem(initial_state)
        
main()


'''
output of initial state should look like
      0   0   0
0 2 3 4 5 6 7 8 9 1
how?
print(f'      {state[10]}   {state[11]}   {state[12]}')
for i in state[:10]:
    print(i, end=' ')
'''