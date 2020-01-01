from typing import List, Union
import unittest

import src as common

"""
Straight forward functionality for sliding specific block once at a time

One can slide a block through UP, DOWN, LEFT and RIGHT directions. For each
direction, there is a corresponding function. While sliding, if there is no
obstacle on the slide direction, the block can be slided successfully.
Otherwise, in case of encountering with an obstacle, None value is returned
representing that the slide operation is unsuccessful. Also, if slide direction
reaches/tries to slide block onto edges, similar to the previous case, None
value is returned.
"""


def slide_block_up(current_state: List[List[int]], rows: int, columns: int, block_to_slide: int) \
        -> Union[None, list, List[List[int]]]:
    updated_state = [row[:] for row in current_state]
    # For each row and column iterate each element
    for i in range(rows):
        for j in range(columns):
            # If target block is found, then try to slide it
            if updated_state[i][j] == block_to_slide:
                # No space left in the direction UP, then return None
                if i <= 0:
                    return None
                else:
                    # If it can move, then check upper cell
                    if updated_state[i - 1][j] != common.EMPTY_CELL_BLOCK:
                        # If the upper cell is not empty then return None
                        return None
                    else:
                        # Otherwise move slide one block up and make its previous position empty
                        updated_state[i - 1][j] = block_to_slide
                        updated_state[i][j] = common.EMPTY_CELL_BLOCK
    return updated_state


def slide_block_down(current_state: List[List[int]], rows: int, columns: int, block_to_slide: int) \
        -> Union[None, list, List[List[int]]]:
    updated_state = [row[:] for row in current_state]
    # For each row and column iterate each element
    for i in range(rows - 1, -1, -1):
        for j in range(columns):
            # If target block is found, then try to slide it
            if updated_state[i][j] == block_to_slide:
                # No space left in the direction DOWN, then return None
                if i >= rows - 1:
                    return None
                else:
                    # If it can move, then check bottom cell
                    if updated_state[i + 1][j] != common.EMPTY_CELL_BLOCK:
                        # If the bottom cell is not empty then return None
                        return None
                    else:
                        # Otherwise move slide one block down and make its previous position empty
                        updated_state[i + 1][j] = block_to_slide
                        updated_state[i][j] = common.EMPTY_CELL_BLOCK
    return updated_state


def slide_block_left(current_state: List[List[int]], rows: int, columns: int, block_to_slide: int) \
        -> Union[None, list, List[List[int]]]:
    updated_state = [row[:] for row in current_state]
    # For each row and column iterate each element
    for j in range(columns):
        for i in range(rows):
            # If target block is found, then try to slide it
            if updated_state[i][j] == block_to_slide:
                # No space left in the direction LEFT, then return None
                if j <= 0:
                    return None
                else:
                    # If it can move, then check left cell
                    if updated_state[i][j - 1] != common.EMPTY_CELL_BLOCK:
                        # If the left cell is not empty then return None
                        return None
                    else:
                        # Otherwise move slide one block left and make its previous position empty
                        updated_state[i][j - 1] = block_to_slide
                        updated_state[i][j] = common.EMPTY_CELL_BLOCK
    return updated_state


def slide_block_right(current_state: List[List[int]], rows: int, columns: int, block_to_slide: int) \
        -> Union[None, list, List[List[int]]]:
    updated_state = [row[:] for row in current_state]  # If there exists any obstacle to move block return empty list
    # For each row and column iterate each element
    for j in range(columns - 1, -1, -1):
        for i in range(rows):
            # If target block is found, then try to slide it
            if updated_state[i][j] == block_to_slide:
                # No space left in the direction RIGHT, then return None
                if j >= columns - 1:
                    return None
                else:
                    # If it can move, then check right cell
                    if updated_state[i][j + 1] != common.EMPTY_CELL_BLOCK:
                        # If the right cell is not empty then return None
                        return None
                    else:
                        # Otherwise move slide one block right and make its previous position empty
                        updated_state[i][j + 1] = block_to_slide
                        updated_state[i][j] = common.EMPTY_CELL_BLOCK
    return updated_state


class StateTransition(unittest.TestCase):

    # Block ids which will be used through all the test cases
    TARGET_BLOCK_ID = 1
    OBSTACLE_BLOCK_ID = 2

    # Test state
    state = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    row = len(state)
    column = len(state[0])

    def test_normal_up_transitions(self):
        for row_index in range(self.row - 1, -1, -1):
            input_state = [x[:] for x in self.state]
            input_state[row_index][1] = self.TARGET_BLOCK_ID

            # Get output state
            output_state = slide_block_up(input_state, self.row, self.column, self.TARGET_BLOCK_ID)
            if row_index - 1 >= 0:
                expected_state = [x[:] for x in self.state]
                expected_state[row_index - 1][1] = self.TARGET_BLOCK_ID
                self.assertListEqual(expected_state, output_state)
            else:
                self.assertIsNone(output_state)

    def test_normal_down_transitions(self):
        for row_index in range(0, self.row):
            input_state = [x[:] for x in self.state]
            input_state[row_index][1] = self.TARGET_BLOCK_ID

            # Get output state
            output_state = slide_block_down(input_state, self.row, self.column, self.TARGET_BLOCK_ID)
            if row_index + 1 < self.row:
                expected_state = [x[:] for x in self.state]
                expected_state[row_index + 1][1] = self.TARGET_BLOCK_ID
                self.assertListEqual(expected_state, output_state)
            else:
                self.assertIsNone(output_state)

    def test_normal_left_transitions(self):
        for column_index in range(self.column - 1, -1, -1):
            input_state = [x[:] for x in self.state]
            input_state[2][column_index] = self.TARGET_BLOCK_ID

            # Get output state
            output_state = slide_block_left(input_state, self.row, self.column, self.TARGET_BLOCK_ID)
            if column_index - 1 >= 0:
                expected_state = [x[:] for x in self.state]
                expected_state[2][column_index - 1] = self.TARGET_BLOCK_ID
                self.assertListEqual(expected_state, output_state)
            else:
                self.assertIsNone(output_state)

    def test_normal_right_transitions(self):
        for column_index in range(0, self.column):
            input_state = [x[:] for x in self.state]
            input_state[2][column_index] = self.TARGET_BLOCK_ID

            # Get output state
            output_state = slide_block_right(input_state, self.row, self.column, self.TARGET_BLOCK_ID)
            if column_index + 1 < self.column:
                expected_state = [x[:] for x in self.state]
                expected_state[2][column_index + 1] = self.TARGET_BLOCK_ID
                self.assertListEqual(expected_state, output_state)
            else:
                self.assertIsNone(output_state)

    def test_obstacled_up_transitions(self):
        input_state = [x[:] for x in self.state]
        input_state[3][1] = self.TARGET_BLOCK_ID
        input_state[2][1] = self.TARGET_BLOCK_ID
        input_state[1][1] = self.OBSTACLE_BLOCK_ID

        # Get output state
        output_state = slide_block_up(input_state, self.row, self.column, self.TARGET_BLOCK_ID)
        self.assertIsNone(output_state)

    def test_obstacled_down_transitions(self):
        input_state = [x[:] for x in self.state]
        input_state[1][1] = self.TARGET_BLOCK_ID
        input_state[2][1] = self.TARGET_BLOCK_ID
        input_state[3][1] = self.OBSTACLE_BLOCK_ID

        # Get output state
        output_state = slide_block_down(input_state, self.row, self.column, self.TARGET_BLOCK_ID)
        self.assertIsNone(output_state)

    def test_obstacled_left_transitions(self):
        input_state = [x[:] for x in self.state]
        input_state[1][2] = self.TARGET_BLOCK_ID
        input_state[1][1] = self.TARGET_BLOCK_ID
        input_state[1][0] = self.OBSTACLE_BLOCK_ID

        # Get output state
        output_state = slide_block_left(input_state, self.row, self.column, self.TARGET_BLOCK_ID)
        self.assertIsNone(output_state)

    def test_obstacled_right_transitions(self):
        input_state = [x[:] for x in self.state]
        input_state[1][0] = self.TARGET_BLOCK_ID
        input_state[1][1] = self.TARGET_BLOCK_ID
        input_state[1][2] = self.OBSTACLE_BLOCK_ID

        # Get output state
        output_state = slide_block_right(input_state, self.row, self.column, self.TARGET_BLOCK_ID)
        self.assertIsNone(output_state)


if __name__ == '__main__':
    unittest.main()
