# slidingpuzzle

[![Documentation Status](https://readthedocs.org/projects/slidingpuzzle/badge/?version=latest)](http://slidingpuzzle.readthedocs.io/?badge=latest)
[![GitHub license](https://img.shields.io/github/license/jmbhughes/slidingpuzzle)](https://github.com/jmbhughes/slidingpuzzle/blob/main/LICENSE.md)
[![codecov](https://codecov.io/gh/jmbhughes/slidingpuzzle/branch/main/graph/badge.svg?token=YZB2ZJ4DIN)](https://codecov.io/gh/jmbhughes/slidingpuzzle)
[![CodeFactor](https://www.codefactor.io/repository/github/jmbhughes/slidingpuzzle/badge)](https://www.codefactor.io/repository/github/jmbhughes/slidingpuzzle)
[![GitHub stars](https://img.shields.io/github/stars/jmbhughes/slidingpuzzle?style=social&label=Star&maxAge=2592000)](https://GitHub.com/jmbhughes/slidingpuzzle/stargazers/)

`slidingpuzzle` is a library that explores the [slidinguzzle game](https://en.wikipedia.org/wiki/Sliding_puzzle). 
It's currently under development and focused on solving the N-puzzle, sometimes also called the N<sup>2</sup>-1 puzzle. 

## Install
1. Clone the repo
2. `pip install .`

## Usage
See [the docs](https://slidingpuzzle.readthedocs.io/en/latest/usage.html)

## Roadmap 
- [x] implement a basic sliding puzzle
- [x] implement a basic N-puzzle
- [x] write a basic BFS solver for N-Puzzle
- [x] write a basic A* solver using the Manhattan heuristic for A*
- [ ] write tests for all the above basics
- [ ] explore the walking distance heuristic
- [ ] explore neural heuristics
- [ ] look into the relaxed version of the N-puzzle where there are k blanks instead of just one
- [ ] implement an unbounded version, so you can push through walls

## Resources:
- [Chalik and Surynek (2019)](http://surynek.net/publications/files/Cahlik-Surynek_Puzzle-ANN_IJCCI-2019.pdf)
on NN for heuristics to solve the puzzle
- [Jenson (2017)](https://medium.com/@prestonbjensen/solving-the-15-puzzle-e7e60a3d9782) 
on solving puzzle with neural heuristic 
- [Kunkle (2001)](http://web.mit.edu/6.034/wwwbob/EightPuzzle.pdf) solving 8-puzzle with minimum moves
- [Reinefeld (?)](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=EE0F7590C155E5065026A36875175739?doi=10.1.1.40.9889&rep=rep1&type=pdf)
on complete solution to 8-puzzle using IDA*
- [CMU assignment with example states and lengths](https://www.andrew.cmu.edu/course/15-121/labs/HW-7%20Slide%20Puzzle/lab.html)
- [Variety of heuristics for solving 8-puzzle](https://cse.iitk.ac.in/users/cs365/2009/ppt/13jan_Aman.pdf)
- [15-puzzle and alternating group by Beeler](https://faculty.etsu.edu/beelerr/fifteen-supp.pdf)
- [15-puzzle solver!](http://kociemba.org/themen/fifteen/fifteensolver.html)
- [Github for another 15 puzzle solver](https://github.com/mwong510ca/15Puzzle_OptimalSolver)
- [Great article by Micheal Kim](https://michael.kim/blog/puzzle) on solving the 15-puzzle
- [Walkthrough of implementing A* to solve N-puzzle](https://algorithmsinsight.wordpress.com/graph-theory-2/a-star-in-general/implementing-a-star-to-solve-n-puzzle/)
- [Walking distance in English](https://web.archive.org/web/20141224035932/http://juropollo.xe0.ru:80/stp_wd_translation_en.htm)
- [Mixing time of the 15-puzzle by Morris and Raymer (2017)](https://projecteuclid.org/journals/electronic-journal-of-probability/volume-22/issue-none/Mixing-time-of-the-fifteen-puzzle/10.1214/16-EJP11.full)
- [Walking distance diagram](https://computerpuzzle.net/english/15puzzle/wd.gif)
