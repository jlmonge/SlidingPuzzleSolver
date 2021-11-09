from collections import deque
import heapq
import time

class Problem: # specifications of the problem
    def __init__(self, initial_state):
        self.initial_state = initial_state # pythonic list of lists representing inital puzzle state
        # pythonic list of lists representing final puzzle state
        self.goal_state = [['A','N','G'],['E','L','I'],['C','A','*']]

    def goal_test(self, state): # returns True if current state is goal state, else False
        return state == self.goal_state
    
        

class Node: # node representing current state of the problem 
    def __init__(self, problem, state, parent=None, heuristic=None):
        self.problem = problem
        self.state = state # pythonic list of lists representing current puzzle state
        self.parent = parent # parent Node
        self.heuristic = heuristic
        # g is cost (since all moves have same cost, this also equals depth)
        # to get to the current node
        if (self.parent == None): # root node
            self.g = 0
        else:
            self.g = parent.g + 1

    @property
    def f(self):
        return self.g + self.h()

    def __lt__(self, other): # used in A*
        return self.f < other.f
    
    '''def __repr__(self): # used in A*
        return str(self.state)'''

    def h(self):
        if self.heuristic == 'misplaced':
            return self.misplaced()
        elif self.heuristic == 'manhattan':
            return self.manhattan()

    def shift_blank_up(self, i, j): # i = row of 0, j = col of 0
        if i != 0 and self.state[i-1][j] != '*': # blank can be shifted up
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap blank with letter
            puzzle_child[i][j], puzzle_child[i-1][j] = puzzle_child[i-1][j], puzzle_child[i][j]
            child = Node(self.problem, puzzle_child, self, self.heuristic) # create Node instance for child
            return child

    def shift_blank_down(self, i, j):
        if i != 2: # blank can be shifted down
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap blank with letter
            puzzle_child[i][j], puzzle_child[i+1][j] = puzzle_child[i+1][j], puzzle_child[i][j]
            child = Node(self.problem, puzzle_child, self, self.heuristic) # create Node instance for child
            return child

    def shift_blank_left(self, i, j):
        if j != 0: # blank can be shifted left
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap blank with letter
            puzzle_child[i][j], puzzle_child[i][j-1] = puzzle_child[i][j-1], puzzle_child[i][j]
            child = Node(self.problem, puzzle_child, self, self.heuristic) # create Node instance for child
            return child

    def shift_blank_right(self, i, j): # (1,0)
        if j != 2: # blank can be shifted right
            puzzle_child = [row[:] for row in self.state] # deep copy puzzle
            # swap blank with letter
            puzzle_child[i][j], puzzle_child[i][j+1] = puzzle_child[i][j+1], puzzle_child[i][j]
            child = Node(self.problem, puzzle_child, self, self.heuristic) # create Node instance for child
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

    def misplaced(self):
        h = 0
        for row in range(3):
            for col in range(3):
                if self.state[row][col] != self.problem.goal_state[row][col]:
                    h += 1
        return h

    def coords_of_val_in_goal_state(self, curr_val): # helper fn for manhattan
        for row in range(3):
            for col in range(3):
                if self.problem.goal_state[row][col] == curr_val:
                    return row, col

    def manhattan(self):
        h = 0
        for row in range(3): # 2
            for col in range(3): # 0
                if self.state[row][col] != self.problem.goal_state[row][col]: # skip m.d. == 0
                    curr_val = self.state[row][col]
                    g_row, g_col = self.coords_of_val_in_goal_state(curr_val)#0,1
                    h += abs(row - g_row) + abs(col - g_col)
        return h

        
class Solver:
    def __init__(self, problem):
        self.problem = problem

    def uniform_cost_search(self):
        initial_node = Node(self.problem, self.problem.initial_state)
        nodes = deque([initial_node]) # pythonic queue for nodes
        seen = set() # nodes whose states have been seen
        seen.add(str(initial_node.state))
        nodes_expanded = 0

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
                    nodes_expanded += 1
                    if self.problem.goal_test(i.state):
                        print("GOAL FOUND @ DEPTH", i.g, "AFTER " +
                            str(nodes_expanded) + " NODES EXPANDED")
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
        initial_node = Node(self.problem, self.problem.initial_state, heuristic=heuristic) # root node
        goal_node = Node(self.problem, self.problem.goal_state, heuristic=heuristic) # goal node
        nodes = [initial_node] # nodes that are yet to be fully explored
        heapq.heapify(nodes)
        seen = set() # nodes whose states have been seen
        seen.add(str(initial_node.state))
        nodes_expanded = 0

        while True:
            if len(nodes) == 0: # every node has been visited
                return None
            node = heapq.heappop(nodes) # pop node with lowest f score
            if self.problem.goal_test(node.state): # go in if goal state achieved
                print("GOAL FOUND @ DEPTH", node.g) 
                for row in node.state:
                    print(row)
                return node
            moves = node.possible_moves()
            for i in moves: # i == type(Node)
                #print(i)
                if i: # if i is None, that means the move wasn't possible, so no point in appending it to nodes
                    nodes_expanded += 1
                    if self.problem.goal_test(i.state):
                        print("GOAL FOUND @ DEPTH", i.g, "AFTER " +
                            str(nodes_expanded) + " NODES EXPANDED")
                        for row in i.state:
                            print(row)
                        return node
                    if str(i.state) not in seen:
                        heapq.heappush(nodes, i)
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
        goal_node = solver.a_star("misplaced")
        path_generator(goal_node,solver)
    elif choice == '3':
        goal_node = solver.a_star("manhattan")
        path_generator(goal_node,solver)
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