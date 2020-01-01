from enum import Enum
from typing import Callable, Dict, List
import unittest

import src as common


class Heuristics(Enum):
    MANHATTAN_DISTANCE = 0
    EUCLIDEAN_DISTANCE = 1


def find_heuristic_function(heuristic_function: int) -> Callable:
    """
    Heuristic function match function
    :param heuristic_function: Integer value of the heuristic function which can be reached from Heuristics enumeration
    :return: Corresponding heuristic function of the given parameter if it is valid; otherwise, exception is raised
    """
    if heuristic_function == Heuristics.MANHATTAN_DISTANCE.value:
        return find_manhattan_distance
    elif heuristic_function == Heuristics.EUCLIDEAN_DISTANCE.value:
        return find_euclidean_distance
    else:
        raise ValueError("Unknown heuristic function value {0}".format(heuristic_function))


def find_manhattan_distance(first_state, second_state):
    """
    This heuristic function calculates manhattan distance for each unique block by checking the most UPPER-LEFT piece
    of them. Formula of manhattan distance is computed as the following.

    .. math:: \sum(coordinate1, coordinate2) = |coordinate1_x-coordinate2_x| + |coordinate1_y-coordinate2_y|
    :param first_state: First state representing the board
    :param second_state: Second state representing the board
    :return: Manhattan distance between states
    """
    first_state_piece_coordinate_dict, second_state_piece_coordinate_dict = _state_traverser(first_state, second_state)
    distance = 0
    for key in first_state_piece_coordinate_dict.keys() & second_state_piece_coordinate_dict.keys():
        x1, y1 = first_state_piece_coordinate_dict[key]
        x2, y2 = second_state_piece_coordinate_dict[key]
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


def find_euclidean_distance(first_state, second_state):
    """
    This heuristic function calculates euclidean distance for each unique block by checking the most UPPER-LEFT piece
    of them. Formula of euclidean distance is computed as the following.

    .. math:: \sum(coordinate1, coordinate2) = \sqrt{(coordinate1_x-coordinate2_x)^2 + (coordinate1_y-coordinate2_y)^2}
    :param first_state: First state representing the board
    :param second_state: Second state representing the board
    :return: Euclidean distance between states
    """
    first_state_piece_coordinate_dict, second_state_piece_coordinate_dict = _state_traverser(first_state, second_state)
    distance = 0
    for key in first_state_piece_coordinate_dict.keys() & second_state_piece_coordinate_dict.keys():
        x1, y1 = first_state_piece_coordinate_dict[key]
        x2, y2 = second_state_piece_coordinate_dict[key]
        distance += ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance


def _state_traverser(first_state: List[List[int]], second_state: List[List[int]]) -> (Dict, Dict):
    """
    State parsing procedure which iterates over two states at the same time and returns two
    dictionaries including the most UPPER-LEFT piece coordinates for each block
    :param first_state: First state representing the board
    :param second_state: Second state representing the board
    :return: Tuple of dictionaries
    """
    first_state_piece_coordinate_dict = {}
    second_state_piece_coordinate_dict = {}

    # Initialize row index as zero at the beginning
    row_index = 0
    for first_row, second_row in zip(first_state, second_state):
        # Initialize column index as zero
        column_index = 0
        for first_block, second_block in zip(first_row, second_row):
            # Put first block if it does not exist
            if first_block != common.EMPTY_CELL_BLOCK and first_block not in first_state_piece_coordinate_dict:
                first_state_piece_coordinate_dict[first_block] = (row_index, column_index)
            # Put first block if it does not exist
            if second_block != common.EMPTY_CELL_BLOCK and second_block not in second_state_piece_coordinate_dict:
                second_state_piece_coordinate_dict[second_block] = (row_index, column_index)
            # Update column index
            column_index += 1
        # Update row index
        row_index += 1

    return first_state_piece_coordinate_dict, second_state_piece_coordinate_dict


class HeuristicFunctionUnittest(unittest.TestCase):
    initial_state = [
        [0, 0, 0],
        [1, 2, 0],
        [0, 3, 3],
        [0, 3, 3]
    ]

    final_state = [
        [3, 3, 0],
        [3, 3, 0],
        [2, 0, 0],
        [1, 0, 0]
    ]

    def test_valid_heuristic_function(self):
        self.assertEquals(find_manhattan_distance, find_heuristic_function(int(Heuristics.MANHATTAN_DISTANCE.value)))
        self.assertEquals(find_euclidean_distance, find_heuristic_function(int(Heuristics.EUCLIDEAN_DISTANCE.value)))

    def test_invalid_heuristic_function(self):
        with self.assertRaises(ValueError) as context:
            find_heuristic_function(int(1e10))

        self.assertEquals(ValueError, type(context.exception))

    def test_manhattan_heuristic(self):
        expected_distance = 7
        output_distance = find_manhattan_distance(self.initial_state, self.final_state)
        self.assertEquals(expected_distance, output_distance)

    def test_euclidean_heuristic(self):
        expected_distance = 5.650281539872885
        output_distance = find_euclidean_distance(self.initial_state, self.final_state)
        self.assertAlmostEqual(expected_distance, output_distance, delta=1e-4)


if __name__ == '__main__':
    unittest.main()
