# Sliding Puzzle Solver

This is a solver for the Angelica puzzle, a type of sliding puzzle. This solver uses uniform cost search and A* search.

## Q: What is the Angelica puzzle?
A: The Angelica puzzle is a 3x3 sliding puzzle where the solution is organized as such:  
![Solution of the Angelica puzzle](/angelicapuzzle.png)  
It is played just like a sliding puzzle, where the asterisk represents a blank space where a tile can be moved.

## Q: What is uniform cost search?
A: Uniform cost search is a type of search that tries to find a path from the start to the goal by expanding the node with the least cost. In the case of the sliding puzzle, the path cost is just the depth.

## Q: What is A* search?
A: A* search is similar to uniform cost search in that the goal is to go from the start to the goal with least cost, however this search does it in a "smarter" manner by using the following estimation function f(n):
```
f(n) = g(n) + h(n)
```
where g(n) is the cost so far to reach node n and h(n) is an estimated cost from node n to the goal node.

## Q: How do you estimate how far a node is from the goal node?
A: This is done with a heuristic. The two I use in this project are the **misplaced tile** heuristic, where the cost equals the number of tiles that are not in the same place as they are in the solution, and the **Manhattan distance** heuristic, where the cost equals the sum of the distance in cardinal moves each tile is from their position in the solution. A* is **the** fastest search algorithm, but the quality of the heuristic determines how quick it really runs.
