# Sliding Block Puzzle Solver

## Problem Description
The problem is sliding blocks puzzle where the main aim is to reach one of the final states
starting from a specific initial state by sliding one block at a time. Each block can slide
in **four** direction if the block which is trying to be slide is not blocked by another block
or edges of board.

Directions are the followings:
1. UP
2. DOWN
3. LEFT
4. RIGHT

The main path finding algorithm used in solution is *A\* Search Algorithm* and among multiple
final states, it will return one of the solution path starting from the initial state to that
final state.

For heuristics of A\* Search Algorithm, **Manhattan Distance** and **Euclidean Distance** are
used where Manhattan Distance is represented with **0** and Euclidean Distance is represented
with **1**.

## Usage
Simply run sliding_block_puzzle.py as the following command
   
```commandline
$ python3 -m src.sliding_block_puzzle -f ./sample_inputs/dict_formatted_inputs/input3.inp
```

## Input Format
There are two input format options that you can use. Before getting into formats, you need to
learn how block are represented. Each block is represented with their unique integer id, i.e.
the same integer values are combined to represent single block.

1. Dictionary like input format: This input format expects heuristic function id, row count,
column count, block count, start state as two dimensional array and final states as list of
two dimensional arrays. You can refer the following sample input.

**Attention**: For parsing, you need to provide keys as expected in the sample input so that
it can be properly parsed. Also, validation of input dimensions are done after reading input
files.

```json
{
    "heuristic_function": 0,
    "row": 4,
    "column": 4,
    "blocks": 15,
    "start_state": [
        [10, 13, 4 , 8 ],
        [2 , 14, 12, 7 ],
        [9 , 0 , 15, 3 ],
        [1 , 5 , 6 , 11]
    ],
    "final_states": [
        [
            [1 , 2 , 3 , 4 ],
            [5 , 6 , 7 , 8 ],
            [9 , 10, 11, 12],
            [13, 14, 15, 0 ]
        ]
    ]
}
```

2. Special plain input format: This input format is specially designed and it was in the following
form. The first line represent heuristic function id. The second line respectively represents row
count, column count, block count and final state count in the same line separated by *space* character.
Then, it expects initial and final states which are separated by *S* and *F* characters. Each state
is written as row by row in each line. And each row consist of its elements separated by *space"
characters.

**Attention**: For parsing, initial state must be placed before final states and also validation of
dimensions of inputs are done after reading inputs. You can refer the following example to figure
out how it is structure 

```
0               # Heuristic function
4 4 15 1        # Row, column, block counts and count of final states
S               # Separator for initial state
10 13 4 8       # Row 1 of initial state
2 14 12 7       # Row 2 of initial state
9 0 15 3        # Row 3 of initial state
1 5 6 11        # Row 4 of initial state
F               # Separator for final states
1 2 3 4         # Row 1 of final state
5 6 7 8         # Row 1 of final state
9 10 11 12      # Row 1 of final state
13 14 15 0      # Row 1 of final state
```
