from __future__ import annotations
import copy
import math
from collections import defaultdict
from queue import PriorityQueue
from typing import List, Optional
from abc import ABC, abstractmethod
from .puzzle import NPuzzle, Action, SlideDirection


class PuzzleNode:
    def __init__(self, puzzle: NPuzzle,
                 children: List[PuzzleNode],
                 actions_to_get_children: List[Action | SlideDirection],
                 parent: Optional[PuzzleNode],
                 action_from_parent: Optional[Action | SlideDirection]):
        self.puzzle = puzzle
        self.children = children
        self.parent = parent
        self.actions_to_get_children = actions_to_get_children
        self.action_from_parent = action_from_parent

    @property
    def depth(self) -> int:
        depth = 0
        current = self
        while current.parent is not None:
            depth += 1
            current = current.parent
        return depth

    def __eq__(self, other: PuzzleNode) -> bool:
        return self.puzzle == other.puzzle and id(self.parent) == id(other.parent) # and self.children == other.children and self.parent == other.parent and self.actions_to_get_children == other.actions_to_get_children and self.action_from_parent == other.action_from_parent

    def __repr__(self) -> str:
        return f"PuzzleNode({self.puzzle}, {self.children}, {self.actions_to_get_children}, {self.parent}, {self.actions_to_get_children}, {self.action_from_parent})"

    def __hash__(self) -> int:
        return hash(self.puzzle)


class NPuzzleHeuristic(ABC):
    @staticmethod
    @abstractmethod
    def h(node: PuzzleNode) -> int:
        pass

    @staticmethod
    def g(node: PuzzleNode) -> int:
        return node.depth

    def f(self, node: PuzzleNode) -> int:
        return self.g(node) + self.h(node)


class ManhattanHeuristic(NPuzzleHeuristic):
    def h(self, node: PuzzleNode) -> int:
        return self._manhattan_distance(node.puzzle)

    @staticmethod
    def _manhattan_distance(puzzle: NPuzzle) -> int:
        return sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
                   for b, g in ((puzzle.placements.index(i), puzzle.solution.index(i))
                                for i in range(1, puzzle.n+1)))


class NPuzzleSolver(ABC):
    def __init__(self, puzzle: NPuzzle):
        assert isinstance(puzzle, NPuzzle), "puzzle must be an NPuzzle"
        self.puzzle = puzzle
        self.solution_node = None
        self.num_nodes_explored = 0

    @abstractmethod
    def solve(self) -> List[SlideDirection] | bool:
        pass

    def _backtrack_solution_node(self) -> List[SlideDirection]:
        if self.solution_node:
            solution = []
            current = self.solution_node
            while current.parent is not None:
                solution.append(current.action_from_parent)
                current = current.parent
            return list(reversed(solution))
        else:
            raise RuntimeError("Cannot backtrack since puzzle is not solved")


class BFSNPuzzleSolver(NPuzzleSolver):
    def solve(self) -> List[SlideDirection] | bool:
        root = PuzzleNode(self.puzzle, [], [], None, None)

        if root.puzzle.is_solved():
            self.solution_node = root
            return self._backtrack_solution_node()
        self.num_nodes_explored += 1

        frontier = [root]
        reached = {self.puzzle}
        while frontier:
            current = frontier.pop(0)
            self.num_nodes_explored += 1
            for slide_direction in SlideDirection:
                child_state = current.puzzle.slide(slide_direction)
                # Expand the tree
                child_node = PuzzleNode(child_state, [], [], current, slide_direction)
                current.children.append(child_node)
                current.actions_to_get_children.append(slide_direction)

                if child_state.is_solved():
                    self.solution_node = child_node
                    return self._backtrack_solution_node()
                if child_state not in reached:
                    reached.add(child_state)
                    frontier.append(child_node)
        return False


class AStarNPuzleSolver(NPuzzleSolver):
    def __init__(self, puzzle: NPuzzle, heuristic: NPuzzleHeuristic):
        super().__init__(puzzle)
        self.heuristic = heuristic

    def solve(self) -> List[SlideDirection] | bool:
        node_id = 0
        start = PuzzleNode(self.puzzle, [], [], None, None)
        nodes = {node_id: start}
        unvisited = PriorityQueue()
        unvisited.put((math.inf, node_id))
        visited = set()

        g_score = defaultdict(lambda: math.inf)
        g_score[start] = 0

        f_score = defaultdict(lambda: math.inf)
        f_score[start] = self.heuristic.h(start)

        while unvisited:
            current = nodes[unvisited.get()[1]]
            self.num_nodes_explored += 1
            if current.puzzle.is_solved():
                self.solution_node = current
                return self._backtrack_solution_node()

            for direction in SlideDirection:
                node_id += 1
                child_puzzle = current.puzzle.slide(direction)
                child = PuzzleNode(child_puzzle, [], [], current, direction)
                current.children.append(child)
                current.actions_to_get_children.append(direction)
                if child_puzzle not in visited:
                    tentative_g_score = g_score[current] + 1

                    if tentative_g_score < g_score[child]:
                        g_score[child] = tentative_g_score
                        f_score[child] = tentative_g_score + self.heuristic.h(child)
                    nodes[node_id] = child
                    unvisited.put((f_score[child], node_id))

            visited.add(current.puzzle)
        return False
