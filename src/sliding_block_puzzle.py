import argparse

import src.heuristic_functions as hf
import src.file_parser as fp


class Puzzle(object):

    def __init__(self, heuristic, row_count, column_count, block_count, initial_state, final_state):
        self.heuristic = hf.find_heuristic_function(heuristic)
        self.row_count = row_count
        self.column_count = column_count
        self.block_count = block_count
        self.initial_state = initial_state
        self.final_state = final_state

    def solve(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='File name to parse and create puzzle',
                        type=argparse.FileType('r'), required=True)
    args = parser.parse_args()

    # Get filename
    _file = args.file

    # Parse puzzle
    puzzle = fp.PuzzleInputParser.parse_dict_formatted_file(_file)

    # Solve puzzle
    puzzle.solve()
