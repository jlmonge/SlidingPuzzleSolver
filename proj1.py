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
   0 0 0  *
2034567891
   0 0 0  *
2304567891
   0 0 0  *
2340567891
   5 0 0  *
2340067891
   5 0 0  *
2346007891
   5 0 0  *
2346700891
   5 8 0  *
2346790001
   5 8 1  *
2346790000
   5 8 1  *
2346700009
   5 0 1  *
2346700089
   5 1 0  *
2346700089
'''

class Problem: # specifications of the problem
    def __init__(self, initial_state):
        self.initial_state = initial_state # pythonic list of lists representing inital puzzle state
        # pythonic list of lists representing final puzzle state
        self.goal_state = [['A','N','G'],['E','L','I'],['C','A','*']]

    def goal_test(self, state): # returns True if current state is goal state, else False
        return state == self.goal_state
    
        

class Node: # node representing current state of the problem 
    def __init__(self, state, parent=None):
        self.state = state # pythonic list of lists representing current puzzle state
        self.parent = parent # parent Node
        # g is cost (since all moves have same cost, this also equals depth)
        # to get to the current node
        if (self.parent == None): # root node
            self.g = 0
        else:
            self.g = parent.g + 1
        self.h = 0
        self.f = 0

    def shift_blank_up(self, i, j): # i = row of 0, j = col of 0
        if i != 0 and self.state[i-1][j] != '*': # blank can be shifted up
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap blank with letter
            puzzle_child[i][j], puzzle_child[i-1][j] = puzzle_child[i-1][j], puzzle_child[i][j]
            child = Node(puzzle_child, self) # create Node instance for child
            return child

    def shift_blank_down(self, i, j):
        if i != 2: # blank can be shifted down
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap blank with letter
            puzzle_child[i][j], puzzle_child[i+1][j] = puzzle_child[i+1][j], puzzle_child[i][j]
            child = Node(puzzle_child, self) # create Node instance for child
            return child

    def shift_blank_left(self, i, j):
        if j != 0: # blank can be shifted left
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap blank with letter
            puzzle_child[i][j], puzzle_child[i][j-1] = puzzle_child[i][j-1], puzzle_child[i][j]
            child = Node(puzzle_child, self) # create Node instance for child
            return child

    def shift_blank_right(self, i, j): # (1,0)
        if j != 2: # blank can be shifted right
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap blank with letter
            puzzle_child[i][j], puzzle_child[i][j+1] = puzzle_child[i][j+1], puzzle_child[i][j]
            child = Node(puzzle_child, self) # create Node instance for child
            return child

    def possible_moves(self):
        poss_moves = []
        for row in range(3):
            for col in range(3):
                if self.state[row][col] == '*':
                    poss_moves.append(self.shift_blank_up(row, col))
                    poss_moves.append(self.shift_blank_down(row, col))
                    poss_moves.append(self.shift_blank_left(row, col))
                    poss_moves.append(self.shift_blank_right(row, col))
        return poss_moves # list of child nodes

    def misplaced(self, goal_node):
        h = 0
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                if self.state[row][col] != goal_node.state[row][col]:
                    h += 1
        return h

        
class Solver:
    def __init__(self, problem):
        self.problem = problem

    def uniform_cost_search(self):
        initial_node = Node(self.problem.initial_state)
        nodes = deque([initial_node]) # pythonic queue for nodes
        seen = set() # nodes whose states have been seen
        seen.add(str(initial_node.state))

        while True:
            if len(nodes) == 0: # every node has been visited
                return None
            node = nodes.popleft() # popleft() for fifo; pop for lifo()
            if self.problem.goal_test(node.state): # go in if goal state achieved
                print("GOAL FOUND @ DEPTH", node.g) 
                for row in node.state:
                    print(row)
                return node
            #nodes = QUEUEING_FUNCTION(nodes, EXPAND(node, problem.OPERATORS)) # for loop
            moves = node.possible_moves()
            for i in moves: # i == type(Node)
                #print(i)
                if i: # if i is None, that means the move wasn't possible, so no point in appending it to nodes
                    if self.problem.goal_test(i.state):
                        print("GOAL FOUND @ DEPTH", i.g) 
                        for row in i.state:
                            print(row)
                        return node
                    if str(i.state) not in seen:
                        nodes.append(i)
                        seen.add(str(i.state))
                        print("DEPTH", i.g) 
                        for row in i.state:
                            print(row)

    def a_star(self, heuristic):
        '''
        if heuristic == "misplaced":
            h = node.misplaced(goal_node)
        '''
        initial_node = Node(self.problem.initial_state)
        goal_node = Node(self.problem.goal_state)
        open_set = deque([initial_node]) # pythonic queue for nodes
        seen = set() # nodes whose states have been seen
        seen.add(str(initial_node.state))
        
        g_list = []

        while True:
            if len(open_set) == 0: # every node has been visited
                return None
            node = open_set.popleft() # popleft() for fifo; pop for lifo()
            if self.problem.goal_test(node.state): # go in if goal state achieved
                print("GOAL FOUND @ DEPTH", node.g) 
                for row in node.state:
                    print(row)
                return node
            moves = node.possible_moves()
            for i in moves: # i == type(Node)
                #print(i)
                if i: # if i is None, that means the move wasn't possible, so no point in appending it to nodes
                    if self.problem.goal_test(i.state):
                        print("GOAL FOUND @ DEPTH", i.g) 
                        for row in i.state:
                            print(row)
                        return node
                    if str(i.state) not in seen:
                        open_set.append(i)
                        seen.add(str(i.state))
                        print("DEPTH", i.g) 
                        for row in i.state:
                            print(row)
            

def user_puzzle():
    """Return a valid puzzle as specified by the user."""
    print("Welcome to the Angelica Puzzle\n" +
        "ANG\n" + 
        "ELI\n" +
        "CA*\n" +
        "*: blank space\n" +
        "*** INSTRUCTIONS ***\n" +
        "There must be 1 asterisk.\n" +
        "All caps.\n" +
        "The input must be able to be rearranged to spell 'ANGELICA*'.\n" + 
        "In each row, each character must be input with a space separating it from the previous/next character.")
    invalid_input = True # must be initialized to True for the validation loop to run
    # split converts input string to list
    first_row = input("Enter the first three characters: ").split()
    second_row = input("Enter the next three characters: ").split()
    third_row = input("Enter the last three characters: ").split()
    user_puzzle = [first_row, second_row, third_row]

    if len(first_row) != 3 or len(second_row) != 3 or len(third_row) != 3: # the input is of invalid length...
        raise Exception("Invalid length") # ...so go back to the start of the loop
    
    valid_angelica_dict = {'A':2,'N':1,'G':1,'E':1,'L':1,'I':1,'C':1,'*':1}
    curr_angelica_dict = {'A':0,'N':0,'G':0,'E':0,'L':0,'I':0,'C':0,'*':0}
    invalid_input = False # now set to False, but set to True again if any conditions are invalid
    for i in range(3):
        for j in range(3):
            curr_char = user_puzzle[i][j]
            if curr_char in curr_angelica_dict and curr_angelica_dict[curr_char] < valid_angelica_dict[curr_char]:
                curr_angelica_dict[curr_char] += 1
            else:
                raise Exception("Invalid input")
    return user_puzzle

def path_generator(goal_node,solver):
    if goal_node:
        print('*' * 20, "generating path", '*' * 20)
        time.sleep(2)
        path = []
        curr_path_node = goal_node
        while curr_path_node != None:
            path.append(curr_path_node)
            curr_path_node = curr_path_node.parent
        
        path.reverse()

        for index in range(len(path)):
            print(f"DEPTH {path[index].g}")
            for row in path[index].state:
                print(row)
        print(f"DEPTH {goal_node.g + 1}: ")
        for row in solver.problem.goal_state:
            print(row)

def user_algorithm(solver):
    """Select an algorithm as specified by the user."""
    choice = input("Enter 1 for Uniform Cost Search, " +
                "2 for A* with the Misplaced Tile heuristic, or " + 
                "3 for A* with the Manhattan Distance heuristic. ")
    if choice == '1':
        goal_node = solver.uniform_cost_search()
        path_generator(goal_node,solver)
                
    elif choice == '2':
        solver.a_star("misplaced")
    elif choice == '3':
        solver.a_star("manhattan")
    else:
        print("please enter a valid entry next time")

def main():
    init_puzzle = user_puzzle() # prompt user for initial state of puzzle
    #init_puzzle = [['A','C','I'],['L','E','G'],['N','A','*']] # sample problem in 536.pdf; depth: 30?
    problem = Problem(init_puzzle) # creates an instance of Problem
    # program dives right into the algorithm selected by user
    solver = Solver(problem)
    user_algorithm(solver)
    #general_search(problem)
        
main()