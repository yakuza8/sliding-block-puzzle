from typing import List, TextIO
from .sliding_block_puzzle import Puzzle


class PuzzleInputParser(object):

    HEURISTIC_LABEL = 'heuristic_function'
    ROW_LABEL = 'row'
    COLUMN_LABEL = 'column'
    BLOCKS_LABEL = 'blocks'
    INITIAL_STATE_LABEL = 'start_state'
    FINAL_STATES_LABEL = 'final_states'

    @staticmethod
    def _validate_inputs(row_count: int, column_count: int, blocks: int,
                         initial_state: List[List[int]], final_states: List[List[List[int]]]):
        all_states = [initial_state] + final_states
        for state in all_states:
            if len(state) != row_count:
                raise ValueError("Given state " + str(state) + " not match in row count.")
            for row in state:
                if len(row) != column_count:
                    raise ValueError("Given state " + str(row) + " not match in column count.")

    @staticmethod
    def parse_dict_formatted_file(f: TextIO):
        puzzle = eval(f.read())

        heuristic = puzzle[PuzzleInputParser.HEURISTIC_LABEL]
        row = puzzle[PuzzleInputParser.ROW_LABEL],
        column = puzzle[PuzzleInputParser.COLUMN_LABEL]
        blocks = puzzle[PuzzleInputParser.BLOCKS_LABEL]
        initial_state = puzzle[PuzzleInputParser.INITIAL_STATE_LABEL]
        final_states = puzzle[PuzzleInputParser.FINAL_STATES_LABEL]

        PuzzleInputParser._validate_inputs()
        return Puzzle(heuristic, row, column, blocks, initial_state, final_states)

    @staticmethod
    def parse_plain_formatted_file(f: TextIO):
        # First line must represent heuristic function id
        heuristic = int(f.readline()[:-1])
        # Second line represents row count, column count, block count and final state count respectively
        row, column, blocks, final_state_count = map(lambda x: int(x), f.readline()[:-1].split())

        states = []
        # There will be one start state but multiple final states
        for state_index in range(0, 1 + final_state_count):
            # No need the information here
            _ = f.readline()

            state = [list(map(lambda x: int(x), f.readline()[:-1].split()))[:column] for _ in range(row)]
            states.append(state)

        initial_state = states[0]
        final_states = states[1:]

        PuzzleInputParser._validate_inputs()
        return Puzzle(heuristic, row, column, blocks, initial_state, final_states)
