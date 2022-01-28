import time
from slidingpuzzle.puzzle import NPuzzle, SlidingPuzzle, SlideDirection
from slidingpuzzle.solver import BFSNPuzzleSolver, ManhattanHeuristic, AStarNPuzleSolver

if __name__ == '__main__':
    puzzle0 = SlidingPuzzle.random_puzzle(3, 3)
    puzzle1 = NPuzzle.random_puzzle(4)
    puzzle2 = NPuzzle(3, [1, 2, 5, 3, 4, 0, 6, 7, 8])
    puzzle3 = NPuzzle(3, [1, 2, 6, 3, 5, 0, 4, 7, 8], solution=[1, 2, 3, 4, 5, 6, 7, 8, 0])
    puzzle4 = NPuzzle(3, [3, 5, 6, 1, 4, 8, 0, 7, 2], solution=[1, 2, 3, 4, 5, 6, 7, 8, 0])
    puzzle5 = NPuzzle(3, [8, 7, 6, 5, 4, 3, 2, 1, 0], solution=[1, 2, 3, 4, 5, 6, 7, 8, 0])
    puzzle6 = NPuzzle(4, [0, 11, 9, 13, 12, 15, 10, 14, 3, 7, 6, 2, 4, 8, 5, 1])
    puzzle7 = NPuzzle(4, [1, 2, 3, 7, 8, 4, 5, 6, 9, 10, 11, 15, 0, 12, 13, 14])
    print(puzzle7)

    solver_bfs = BFSNPuzzleSolver(puzzle7)
    solver_astar = AStarNPuzleSolver(puzzle7, ManhattanHeuristic())
    if puzzle6.is_solvable():
        bfs_start = time.time()
        solution_bfs = solver_bfs.solve()
        print("BFS", solver_bfs.num_nodes_explored)
        bfs_end = time.time()
        bfs_duration = bfs_end - bfs_start
        print(bfs_duration, len(solution_bfs), solution_bfs)

        astar_start = time.time()
        solution_astar = solver_astar.solve()
        print("A*", solver_astar.num_nodes_explored)
        astar_end = time.time()
        astar_duration = astar_end - astar_start
        print(astar_duration, len(solution_astar), solution_astar)

        print()
        print("Node ratio:", solver_bfs.num_nodes_explored / solver_astar.num_nodes_explored)
        print("Speed ratio", bfs_duration / astar_duration)
    else:
        print("Not solvable")
