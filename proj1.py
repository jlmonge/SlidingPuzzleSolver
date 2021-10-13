def general_search(problem, QUEUEING_FUNCTION)
    nodes = MAKE_QUEUE(MAKE_NODE(problem, INITIAL_STATE))   # could be a list

    while True:
        if len(nodes) == 0:
            return "Failure"
        node = REMOVE_FRONT(nodes)  # nodes.pop()
        if problem.GOAL_TEST(node.STATE):
            return node
        nodes = QUEUEING_FUNCTION(nodes, EXPAND(node, problem, OPERATORS))