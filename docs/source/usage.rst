Usage
=====

.. _installation:

Installation
------------

To use Lumache, first clone the repo and then install it using pip:

.. code-block:: console
   (.venv) $ git clone https://github.com/jmbhughes/slidingpuzzle.git
   (.venv) $ pip install .

Some day it might be available on PyPI.

Creating a puzzle
-----------------
To create a predefined ``NPuzzle``, you use a list defining the size, the configuration, and the solution.
For example:

>>> import slidingpuzzle as sp
>>> my_puzzle =  sp.NPuzzle(3, [1, 2, 6, 3, 5, 0, 4, 7, 8], solution=[1, 2, 3, 4, 5, 6, 7, 8, 0])

Alternatively, you can generate a random puzzle.

.. autofunction:: slidingpuzzle.NPuzzle.random_puzzle(3)

To solve, you can use breadth-first search (BFS) or A*. The syntax is the same. For A*:

>>> import slidingpuzzle as sp
>>> my_puzzle = sp.NPuzzle.random_puzzle(3)
>>> solver_bfs = sp.AStarNPuzleSolver(my_puzzle, sp.ManhattanHeuristic())
>>> solution_bfs = solver_bfs.solve()
>>> print(solution_bfs)


