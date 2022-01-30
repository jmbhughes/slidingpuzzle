import pytest
import copy
from slidingpuzzle.puzzle import *


def test_slide_directions():
    assert len(SlideDirection) == 4
    assert str(SlideDirection.DOWN) == "DOWN"
    assert str(SlideDirection.RIGHT) == "RIGHT"
    assert str(SlideDirection.LEFT) == "LEFT"
    assert str(SlideDirection.UP) == "UP"


@pytest.mark.parametrize("n_rows,n_cols",
                          [(3, 3),
                           (3, 4),
                           (4, 3),
                           (4, 4)])
def test_generate_random_puzzle_placements(n_rows, n_cols):
    placements = generate_random_puzzle_placements(n_rows, n_cols)
    assert len(placements) == n_rows * n_cols
    assert set(placements) == set(range(n_rows * n_cols))


@pytest.fixture
def almost_solved_sliding_puzzle():
    placements = [1, 0, 2, 3, 4, 5, 6, 7, 8]
    return SlidingPuzzle(3, 3, placements)


@pytest.fixture
def multiple_blanks_sliding_puzzle():
    placements = [0, 0, 0, 1, 2, 3, 4, 5, 6]
    solution = [0, 0, 0, 1, 2, 3, 4, 5, 6]
    return SlidingPuzzle(3, 3, placements, solution=solution)


def test_sliding_puzzle_initialization(almost_solved_sliding_puzzle):
    assert almost_solved_sliding_puzzle.n_cols == 3
    assert almost_solved_sliding_puzzle.n_rows == 3
    assert almost_solved_sliding_puzzle.placements == [1, 0, 2, 3, 4, 5, 6, 7, 8]
    assert almost_solved_sliding_puzzle.solution == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert len(almost_solved_sliding_puzzle) == 9
    assert str(almost_solved_sliding_puzzle) == "1\t\t2\t\n3\t4\t5\t\n6\t7\t8\t\n"


def test_sliding_puzzle_get(almost_solved_sliding_puzzle):
    assert almost_solved_sliding_puzzle.get(0, 0) == 1
    assert almost_solved_sliding_puzzle.get(0, 1) == 0
    assert almost_solved_sliding_puzzle.get(0, 2) == 2
    counter = 3
    for row in range(1, 3):
        for col in range(3):
            assert almost_solved_sliding_puzzle.get(row, col) == counter
            counter += 1


@pytest.mark.parametrize("n_rows,n_cols",
                          [(3, 3),
                           (3, 4),
                           (4, 3),
                           (4, 4)])
def test_sliding_puzzle_random_generation(n_rows, n_cols):
    puzzle = SlidingPuzzle.random_puzzle(n_rows, n_cols)
    assert puzzle.n_rows == n_rows
    assert puzzle.n_cols == n_cols
    assert len(puzzle.placements) == n_rows * n_cols
    assert set(puzzle.placements) == set(range(n_rows * n_cols))


def test_sliding_puzzle_is_empty(almost_solved_sliding_puzzle):
    assert almost_solved_sliding_puzzle.is_empty(0, 1)
    for row in range(3):
        for col in range(3):
            if (row, col) != (0, 1):
                assert not almost_solved_sliding_puzzle.is_empty(row, col)


def test_sliding_puzzle_is_full(almost_solved_sliding_puzzle):
    assert not almost_solved_sliding_puzzle.is_full(0, 1)
    for row in range(3):
        for col in range(3):
            if (row, col) != (0, 1):
                assert almost_solved_sliding_puzzle.is_full(row, col)


def test_normal_sliding_puzzle_get_blank_positions(almost_solved_sliding_puzzle):
    assert almost_solved_sliding_puzzle.get_blank_positions() == [(0, 1)]


def test_multiple_blanks_sliding_puzzle_get_blank_positions(multiple_blanks_sliding_puzzle):
    assert multiple_blanks_sliding_puzzle.get_blank_positions() == [(0, 0), (0, 1), (0, 2)]


def test_sliding_puzzle_is_solved(multiple_blanks_sliding_puzzle, almost_solved_sliding_puzzle):
    assert not almost_solved_sliding_puzzle.is_solved()
    assert multiple_blanks_sliding_puzzle.is_solved()


def test_sliding_puzzle_slide(almost_solved_sliding_puzzle):
    action = Action(0, 0, 0, 1)
    result = almost_solved_sliding_puzzle.slide(action)
    assert isinstance(result, SlidingPuzzle)
    assert result.is_solved()

    action = Action(0, 1, 0, 0)
    with pytest.raises(AssertionError):
        almost_solved_sliding_puzzle.slide(action)


def test_sliding_puzzle_legal_start_end(almost_solved_sliding_puzzle):
    assert not almost_solved_sliding_puzzle._legal_start_end(0, -1, 0, 0)
    assert not almost_solved_sliding_puzzle._legal_start_end(0, 0, 0, -1)
    assert not almost_solved_sliding_puzzle._legal_start_end(0, 0, 0, 2)
    assert almost_solved_sliding_puzzle._legal_start_end(0, 0, 1, 0)
    assert not almost_solved_sliding_puzzle._legal_start_end(0, 0, 2, 0)
    assert not almost_solved_sliding_puzzle._legal_start_end(0, 1, 2, 2)


def test_sliding_puzzle_equals():
    # should be equal
    placements = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    solution = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert SlidingPuzzle(3, 3, placements, solution) == SlidingPuzzle(3, 3, placements, solution)

    # rows and columns are not equal
    assert SlidingPuzzle(1, 9, placements, solution) != SlidingPuzzle(3, 3, placements, solution)

    # solutions are not equal
    solution2 = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    assert SlidingPuzzle(3, 3, placements, solution) != SlidingPuzzle(3, 3, placements, solution2)

    # placements are not equal
    placements2 = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    assert SlidingPuzzle(3, 3, placements, solution) != SlidingPuzzle(3, 3, placements2, solution)


def test_sliding_puzzle_repr(almost_solved_sliding_puzzle):
    out = "SlidingPuzzle(3, 3, [1, 0, 2, 3, 4, 5, 6, 7, 8], solution=[0, 1, 2, 3, 4, 5, 6, 7, 8])"
    assert repr(almost_solved_sliding_puzzle) == out


def test_sliding_puzzle_hash(almost_solved_sliding_puzzle, multiple_blanks_sliding_puzzle):
    assert hash(almost_solved_sliding_puzzle) != hash(multiple_blanks_sliding_puzzle)


def test_sliding_puzzle_copy(almost_solved_sliding_puzzle):
    my_copy = copy.copy(almost_solved_sliding_puzzle)
    assert isinstance(my_copy, SlidingPuzzle)
    assert almost_solved_sliding_puzzle == my_copy


def test_sliding_puzzle_deep_copy(almost_solved_sliding_puzzle):
    my_deep_copy = copy.deepcopy(almost_solved_sliding_puzzle)
    assert almost_solved_sliding_puzzle == my_deep_copy
    assert isinstance(my_deep_copy, SlidingPuzzle)
    assert id(almost_solved_sliding_puzzle) != id(my_deep_copy)


@pytest.fixture
def example_npuzzle1():
    """ an easily solvable puzzle by moving left"""
    placements = [1, 0, 2, 3, 4, 5, 6, 7, 8]
    solution = [1, 2, 0, 3, 4, 5, 6, 7, 8]
    return NPuzzle(3, placements, solution)


@pytest.fixture
def example_npuzzle2():
    """ an impossible to solve puzzle"""
    placements = [2, 0, 1, 3, 4, 5, 6, 7, 8]
    solution = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    return NPuzzle(3, placements, solution)

def test_npuzzle_initialization(example_npuzzle1):
    assert example_npuzzle1.n_cols == 3
    assert example_npuzzle1.n_rows == 3
    assert example_npuzzle1.n == 8
    assert example_npuzzle1.placements == [1, 0, 2, 3, 4, 5, 6, 7, 8]
    assert example_npuzzle1.solution == [1, 2, 0, 3, 4, 5, 6, 7, 8]
    assert len(example_npuzzle1) == 9
    assert str(example_npuzzle1) == "1\t\t2\t\n3\t4\t5\t\n6\t7\t8\t\n"


@pytest.mark.parametrize("width", [3, 4, 5])
def test_npuzzle_random_generation(width):
    puzzle = NPuzzle.random_puzzle(width)
    assert puzzle.n_rows == width
    assert puzzle.n_cols == width
    assert puzzle.n == width**2 - 1
    assert len(puzzle.placements) == width * width
    assert set(puzzle.placements) == set(range(width * width))


def test_npuzzle_slide(example_npuzzle1):
    result = example_npuzzle1.slide(SlideDirection.LEFT)
    assert isinstance(result, NPuzzle)
    assert result.is_solved()

    second_result = result.slide(SlideDirection.LEFT)
    assert result == second_result


def test_npuzzle_is_solvable(example_npuzzle1, example_npuzzle2):
    assert example_npuzzle1.is_solvable()
    assert not example_npuzzle2.is_solvable()
    solutions = {
        3: [1, 2, 3, 4, 5, 6, 7, 8, 0],
        4: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    }
    solvable_puzzles = [NPuzzle(3, [1, 2, 5, 3, 4, 0, 6, 7, 8], solution=solutions[3]),
                        NPuzzle(3, [1, 2, 6, 3, 5, 0, 4, 7, 8], solution=solutions[3]),
                        NPuzzle(3, [3, 5, 6, 1, 4, 8, 0, 7, 2], solution=solutions[3]),
                        NPuzzle(3, [8, 7, 6, 5, 4, 3, 2, 1, 0], solution=solutions[3]),
                        NPuzzle(4, [0, 11, 9, 13, 12, 15, 10, 14, 3, 7, 6, 2, 4, 8, 5, 1], solution=solutions[4]),
                        NPuzzle(4, [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13, 0, 14, 15], solution=solutions[4])]

    for puzzle in solvable_puzzles:
        assert puzzle.is_solvable()


def test_npuzzle_inversion_count(example_npuzzle2):
    assert example_npuzzle2._get_inv_count() == 1


def test_npuzzle_get_blank_row(example_npuzzle1):
    assert example_npuzzle1._find_blank_row_from_bottom() == 3


def test_npuzzle_copy(example_npuzzle1):
    my_copy = copy.copy(example_npuzzle1)
    assert isinstance(my_copy, NPuzzle)
    assert example_npuzzle1 == my_copy


def test_npuzzle_deep_copy(example_npuzzle1):
    my_deep_copy = copy.deepcopy(example_npuzzle1)
    assert example_npuzzle1 == my_deep_copy
    assert isinstance(my_deep_copy, NPuzzle)
    assert id(example_npuzzle1) != id(my_deep_copy)