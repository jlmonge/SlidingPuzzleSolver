from collections import deque

class Problem:
    def __init__(self):
        self.initial_state = "state"

def general_search(problem, QUEUEING_FUNCTION):
    nodes = deque(MAKE_NODE(problem.initial_state))    # deque

    while True:
        if len(nodes) == 0:
            return "Failure"
        node = REMOVE_FRONT(nodes)  # nodes.pop()
        if problem.GOAL_TEST(node.STATE):
            return node
        nodes = QUEUEING_FUNCTION(nodes, EXPAND(node, problem.OPERATORS))