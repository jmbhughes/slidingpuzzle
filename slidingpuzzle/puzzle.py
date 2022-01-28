from __future__ import annotations
from typing import Optional, Tuple, List
from enum import Enum
import random
from collections import namedtuple
import copy


Action = namedtuple("Action", "start_row start_col end_row end_col")


class SlideDirection(Enum):
    """
    The potential slide directions for a normal N-Puzzle.
    """
    DOWN = (-1, 0)
    LEFT = (0, 1)
    RIGHT = (0, -1)
    UP = (1, 0)

    def __str__(self):
        return f"{self.value}"


def generate_random_puzzle_placements(n_rows: int, n_cols: int):
    assert n_rows > 0, "Must be at least one row"
    assert n_cols > 0, "Must be at least one column"
    placements = list(range(n_rows * n_cols))
    random.shuffle(placements)
    return placements


class SlidingPuzzle:
    def __init__(self, n_rows: int, n_cols: int, placements: List[int], solution: Optional[List[int]] = None):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.placements = placements
        if solution:
            self.solution = solution
        else:
            self.solution = self._generate_solution()

    def _legal_start_end(self, start_row, start_col, end_row, end_col):
        if not self._legal_coordinate(start_row, start_col):
            return False
        if not self._legal_coordinate(end_row, end_col):
            return False

        if start_row == end_row:
            if abs(start_col - end_col) == 1:
                return True
            else:
                return False
        elif start_col == end_col:
            if abs(start_row - end_row) == 1:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def random_puzzle(cls, n_rows: int, n_cols: int):
        placements = generate_random_puzzle_placements(n_rows, n_cols)
        return cls(n_rows, n_cols, placements)

    def _generate_solution(self) -> List[int]:
        return list(range(self.n_rows * self.n_cols))

    def _legal_coordinate(self, row: int, col: int):
        return 0 <= row < self.n_rows and 0 <= col < self.n_cols

    def _get_internal_coordinate(self, row: int, col: int) -> int:
        return self.n_cols * row + col

    def get(self, row: int, col: int) -> int:
        assert self._legal_coordinate(row, col)
        index = self._get_internal_coordinate(row, col)
        return self.placements[index]

    def is_empty(self, row: int, col: int) -> bool:
        return self.get(row, col) == 0

    def is_full(self, row: int, col: int) -> bool:
        return not self.is_empty(row, col)

    def get_blank_positions(self) -> List[Tuple[int, int]]:
        positions = []
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                if self.is_empty(row, col):
                    positions.append((row, col))
        return positions

    def slide(self, action: Action) -> SlidingPuzzle:
        assert isinstance(action, Action), "action must be an Action type"
        assert self._legal_start_end(action.start_row, action.start_col, action.end_row, action.end_col)
        assert self.is_empty(action.end_row, action.end_col)
        assert self.is_full(action.start_row, action.start_col)

        output = self.__deepcopy__()
        index = output._get_internal_coordinate(action.start_row, action.start_col)
        number = output.get(action.start_row, action.start_col)
        output.placements[index] = 0

        index = output._get_internal_coordinate(action.end_row, action.end_col)
        output.placements[index] = number
        return output

    def is_solved(self) -> bool:
        return self.placements == self.solution

    def __len__(self) -> int:
        return self.n_rows * self.n_cols

    def __str__(self) -> str:
        output = ""
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                number = self.get(row, col)
                output += str(number) + "\t" if number != 0 else "" + "\t"
            output += "\n"
        return output

    def __eq__(self, other: SlidingPuzzle) -> bool:
        return self.n_rows == other.n_rows and self.n_cols == other.n_cols \
               and self.placements == other.placements and self.solution == other.solution

    def __repr__(self) -> str:
        return f"TileGrid({self.n_rows}, {self.n_cols}, {self.placements}, solution={self.solution})"

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __copy__(self) -> SlidingPuzzle:
        return SlidingPuzzle(self.n_rows, self.n_cols, self.placements, self.solution)

    def __deepcopy__(self, memodict={}):
        return SlidingPuzzle(copy.deepcopy(self.n_rows, memodict),
                             copy.deepcopy(self.n_cols, memodict),
                             copy.deepcopy(self.placements, memodict),
                             copy.deepcopy(self.solution, memodict))


class NPuzzle(SlidingPuzzle):
    def __init__(self, width: int, placements: List[int], solution: Optional[List[int]] = None):
        super().__init__(width, width, placements, solution)
        self.n = width**2 - 1

    @classmethod
    def random_puzzle(cls, width: int):
        placements = generate_random_puzzle_placements(width, width)
        return cls(width, placements)

    def _get_inv_count(self) -> int:
        inv_count = 0
        for i in range(self.n):
            for j in range(i + 1, self.n+1):
                # count pairs(arr[i], arr[j]) such that
                # i < j and arr[i] > arr[j]
                if self.placements[j] and self.placements[i] and self.placements[i] > self.placements[j]:
                    inv_count += 1
        return inv_count

    # find Position of blank from bottom
    def _find_x_row_from_bottom(self) -> int:
        # start from bottom-right corner of matrix
        for i in range(self.n_rows - 1, -1, -1):
            for j in range(self.n_rows - 1, -1, -1):
                if self.is_empty(i, j):
                    return self.n_rows - i

    # This function returns true if given
    # instance of N*N - 1 puzzle is solvable
    def is_solvable(self) -> bool:
        # Count inversions in given puzzle
        inv_count = self._get_inv_count()

        # If grid is odd, return true if inversion count is even.
        if self.n_rows % 2 == 1:
            return inv_count % 2 == 0
        else:  # grid is even
            pos = self._find_x_row_from_bottom()
            if pos % 2 == 0:
                return inv_count % 2 == 1
            else:
                return inv_count % 2 == 0

    def slide(self, direction: SlideDirection) -> NPuzzle:
        assert isinstance(direction, SlideDirection), "direction must be a SlideDirection type"
        delta_row, delta_col = direction.value
        resulting_puzzle = copy.deepcopy(self)
        blank_positions: List[Tuple[int, int]] = resulting_puzzle.get_blank_positions()
        for blank_row, blank_col in blank_positions:
            start_row, start_col = blank_row + delta_row, blank_col + delta_col
            if resulting_puzzle._legal_coordinate(start_row, start_col):
                action = Action(start_row, start_col, blank_row, blank_col)
                index = resulting_puzzle._get_internal_coordinate(action.start_row, action.start_col)
                number = resulting_puzzle.get(action.start_row, action.start_col)
                resulting_puzzle.placements[index] = 0

                index = resulting_puzzle._get_internal_coordinate(action.end_row, action.end_col)
                resulting_puzzle.placements[index] = number
        return resulting_puzzle

    def __copy__(self) -> NPuzzle:
        return NPuzzle(self.n_cols, self.placements, self.solution)

    def __deepcopy__(self, memodict={}) -> NPuzzle:
        return NPuzzle(copy.deepcopy(self.n_cols, memodict),
                       copy.deepcopy(self.placements, memodict),
                       copy.deepcopy(self.solution, memodict))
