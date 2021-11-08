from collections import deque
import heapq
import time

# optimal solution: https://www.youtube.com/watch?v=o4ZDw9oFlP8

'''
Moves used in optimal result:
1. out of trench (if possible, all the way left/right OR into another trench)
2. into trench
3. all the way left/right
This is fine; the instructions say that a man may go any distance
that is possible in a move, so I decided it would be best for the men
to move only in optimal moves, as used in the optimal solution. 
'''

'''
DEPTH 0
   0 0 0
0234567891

DEPTH 1
   4 0 0
0230567891
   0 6 0
0234507891
   0 0 8
0234567091
   0 0 0
2034567891
'''

class Problem: # specifications of the problem
    def __init__(self, initial_state):
        self.initial_state = initial_state # pythonic list of lists representing inital positions of men
        # pythonic list representing final positions of men
        self.goal_state = [[' ',' ',' ',0,' ',0,' ',0,' ',' '],[1,2,3,4,5,6,7,8,9,0]]

    def goal_test(self, state): # returns True if current state is goal state, else False
        return state == self.goal_state
    
        

class Node: # node representing current state of the problem 
    def __init__(self, state, parent=None):
        self.state = state # list of current positions of men
        self.parent = parent # parent Node
        # g is cost (since all moves have same cost, this also equals depth)
        # to get to the current node
        if (self.parent == None): # root node
            self.g = 0
        else:
            self.g = parent.g + 1

    '''def __str__(self):
        l1 = []
        for row in range(2):
            for col in range(10):
                l1.append(self.state[i][j])
        return [' ']'''

    def shift_zero_up(self, i, j): # i = row of 0, j = col of 0
        if i == 1 and self.state[i-1][j] != ' ': # zero can be shifted up
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap 0 with soldier
            puzzle_child[i][j], puzzle_child[i-1][j] = puzzle_child[i-1][j], puzzle_child[i][j]
            child = Node(puzzle_child, self) # create Node instance for child
            return child

    def shift_zero_down(self, i, j):
        if i == 0: # zero can be shifted down
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap 0 with soldier
            puzzle_child[i][j], puzzle_child[i+1][j] = puzzle_child[i+1][j], puzzle_child[i][j]
            child = Node(puzzle_child, self) # create Node instance for child
            return child

    def shift_zero_left(self, i, j):
        if i == 1 and j > 0: # zero can be shifted left
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap 0 with soldier
            puzzle_child[i][j], puzzle_child[i][j-1] = puzzle_child[i][j-1], puzzle_child[i][j]
            child = Node(puzzle_child, self) # create Node instance for child
            return child

    def shift_zero_right(self, i, j): # (1,0)
        if i == 1 and j < 9: # zero can be shifted right
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap 0 with soldier
            puzzle_child[i][j], puzzle_child[i][j+1] = puzzle_child[i][j+1], puzzle_child[i][j]
            child = Node(puzzle_child, self) # create Node instance for child
            return child

    '''def first_to_first(self, i, j):
        while 

    def first_to_second(self, i, j):
        print("hello")
    
    def second_to_first(self, i, j):
        print("hello")
    
    def second_to_second(self, i, j):
        print("hello")'''

    def possible_moves(self):
        poss_moves = []
        for row in range(2):
            for col in range(10):
                if self.state[row][col] == 0:
                    poss_moves.append(self.shift_zero_up(row, col))
                    poss_moves.append(self.shift_zero_down(row, col))
                    poss_moves.append(self.shift_zero_left(row, col))
                    poss_moves.append(self.shift_zero_right(row, col))
        return poss_moves
        
class Solver:
    def __init__(self, problem):
        self.problem = problem

    def uniform_cost_search(self):
        initial_node = Node(self.problem.initial_state)
        print(initial_node.state, initial_node.g)
        nodes = deque([initial_node]) # pythonic queue for nodes
        seen = set() # nodes whose states have been seen
        seen.add(str(initial_node.state))

        while True:
            if len(nodes) == 0: # every node has been visited
                return "Failure"
            node = nodes.popleft() # popleft() for fifo; pop for lifo()
            if self.problem.goal_test(node.state): # go in if goal state achieved
                return node
            #nodes = QUEUEING_FUNCTION(nodes, EXPAND(node, problem.OPERATORS)) # for loop
            moves = node.possible_moves()
            for i in moves:
                #print(i)
                if i:
                    if str(i.state) not in seen:
                        nodes.append(i)
                        seen.add(str(i.state))
                        print(i.state, i.g)
            #time.sleep(10)

            

def user_puzzle():
    """Return a valid puzzle as specified by the user."""
    print("Welcome to Nine Men in a Trench\n" +
        "   0 0 0  \n" +
        "1234567890\n" +
        "0: blank space\n" +
        "1: sergeant\n" +
        "2-9: other men in the trench\n" +
        "*** INSTRUCTIONS ***\n" +
        "There must be 4 blank spaces.\n" +
        "Each positive number must be used once.\n" + 
        "Each number must be entered with a space separating it from the previous/next number.")
    invalid_input = True # must be initialized to True for the validation loop to run
    while invalid_input: # validation loop; if True, then input is invalid and loop must continue
        # split converts input string to list
        first_row = input("Enter the first row (3 entries): ").split()
        second_row = input("Enter the second row (10 entries): ").split()

        if len(first_row) != 3 or len(second_row) != 10: # the input is of invalid length...
            continue # ...so go back to the start of the loop

        num_blanks = 0 # number of empty spaces throughout the puzzle; prevents input of excess zeros
        positive_set = set() # set of all positive numbers seen so far; prevents duplicate positive numbers
        invalid_input = False # now set to False, but set to True again if any conditions are invalid
        for i in range(3): # inspect first row
            first_row[i] = int(first_row[i]) # if input was non-numerical, this will raise an error
            if first_row[i] == 0: # current space is 0
                num_blanks += 1
            elif (first_row[i] > 0 and first_row[i] < 10 and 
                    first_row[i] not in positive_set): # current space is a unique number 1-9
                positive_set.add(first_row[i])
            else:
                invalid_input = True
                break
        for i in range(10): # inspect second row
            second_row[i] = int(second_row[i])
            if second_row[i] == 0 and num_blanks < 5: # current space is 0 and there are no more than 4 0's
                num_blanks += 1
            elif (second_row[i] > 0 and second_row[i] < 10 and 
                    second_row[i] not in positive_set): # current space is a unique number 1-9
                positive_set.add(second_row[i])
            else:
                invalid_input = True
                break
    first_row = [' ',' ',' ',first_row[0],' ',first_row[1],' ',first_row[2],' ',' ']
    user_puzzle = [first_row, second_row]
    return user_puzzle

def user_algorithm(solver):
    """Select an algorithm as specified by the user."""
    choice = input("Enter 1 for Uniform Cost Search, " +
                "2 for A* with the Misplaced Tile heuristic, or " + 
                "3 for A* with the Manhattan Distance heuristic. ")
    if choice == '1':
        solver.uniform_cost_search()
    elif choice == '2':
        solver.a_star()
    elif choice == '3':
        solver.a_star()
    else:
        print("please enter a valid entry next time")

def main():
    #init_puzzle = user_puzzle() # prompt user for initial state of puzzle
    init_puzzle = [[' ',' ',' ',0,' ',0,' ',0,' ',' '],[0,2,3,4,5,6,7,8,9,1]]
    problem = Problem(init_puzzle) # creates an instance of Problem
    # program dives right into the algorithm selected by user
    solver = Solver(problem)
    user_algorithm(solver)
    #general_search(problem)
        
main()