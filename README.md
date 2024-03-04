# TSP Solver

This repository contains a Python implementation of a Traveling Salesman Problem (TSP) solver using the steepest hill climbing algorithm with restart and tabou search.
This project was developed as part of a practical work assignment for my "Advanced Algorithmics" class during the first semester of my master's degree (Data Science degree at University Paul Sabatier of Toulouse). It served as an opportunity to deepen my understanding of metaheuristics and their applications to classic problems like the TSP.

For more information and context, you can access the assignement description and my personal project report, both in French, available in the root of this repository.

## Overview

The Traveling Salesman Problem (TSP) is a classic optimization problem in which a salesman aims to find the shortest possible route that visits each city exactly once and returns to the original city. This implementation provides solutions to the TSP using two approaches:

1. **Steepest Hill Climbing with Restart**: This algorithm iteratively explores neighboring solutions and moves to the best neighboring solution until no improvement is found within a specified number of iterations. Then, it restarts the search from different initial solutions to potentially escape local optima.

2. **Steepest Hill Climbing with tabou Search**: This variant incorporates a tabou list to prevent revisiting previously visited solutions. It explores neighboring solutions while avoiding those in the tabou list, aiming to find better solutions.

## Features

- Implements steepest hill climbing algorithms for TSP.
- Provides options for using either steepest hill climbing with restart or tabou search.
- Supports customizations such as maximum number of iterations and tabou list size.
- Outputs the best solution found along with its value and number of iterations.

## Usage

```
python3 mh_tsp.py <filepath>
```

Replace `<filepath>` with the path to your TSP data file. The data file should contain the number of cities followed by the coordinates of each city.

## Example

Several TSP data files are already provided in the directory `instances/`. Example:
```
python3 mh_tsp.py instances/tsp25.txt
```

## Room for Improvement

A key enhancement would involve enabling to select different operational modes, such as with/without restart or tabou search, directly from the command line when running the program. By implementing these improvements, users will have greater flexibility and ease of interaction with the TSP solver, without the need to modify the source code.

## Additional Notes

- This README.md was created with the assistance of ChatGPT 3.5.

- As a learning project, the focus was on applying algorithmic concepts rather than producing perfectly polished code.

## License

This project is licensed under the MIT License.
