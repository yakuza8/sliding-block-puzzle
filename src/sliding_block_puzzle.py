import argparse
from typing import List, Tuple, Union

import src.heuristic_functions as hf
import src.file_parser as fp
import src.state_transitions as st


class Node(object):
    """
    Node structure of a state at a specific instant
    State = Board state of the node
    Parent = Parent state of the node where the current node is expanded
    G Value = Accumulated cost of the current node starting from the initial node
    F Value = The expected cost with respect to heuristic function and G value
    """

    def __init__(self, state: List[List[int]], parent, g_value: int, f_value: int):
        self.state = state
        self.parent = parent
        self.g_value = g_value
        self.f_value = f_value


class Puzzle(object):

    INITIAL_G_VALUE = 0

    def __init__(self, heuristic, row_count: int, column_count: int, block_count: int,
                 initial_state: List[List[int]], final_states: List[List[List[int]]]):
        self.heuristic_function = hf.find_heuristic_function(heuristic)
        self.row_count = row_count
        self.column_count = column_count
        self.block_count = block_count
        self.initial_state = initial_state
        self.final_states = final_states

    def solve(self):
        """
        A* Search Pseudo Algorithm
        ==========================
        Symbols: OPEN: S: Start state, Open state, CLOSED: Closed states, G: Goal states, f_value = h_value + g_value,
                 h_value = cost value what heuristic function computes,
                 g_value = accumulated cost value from start node to the current node

        1) Initialize OPEN <- {S} and CLOSED <- EMPTY_SET
        2) If OPEN = EMPTY_SET then return FAILURE
        3) Find minimum f-valued node among OPEN states
            * node <- arg min(f_value(t)) where t in OPEN
            * OPEN <- OPEN - {node}
            * CLOSED <- CLOSED + {node}
        4) If node in G, then return the solution path by using parent information from node to S
        5) Otherwise, expand node to its successor as N
        6) For each node' in N
            * If node' not in OPEN and node' not in CLOSED, then insert node' into OPEN setting its parent node
            * Else, if it is in OPEN, then check and update g value. Otherwise, it is in CLOSED, then do the same checks
            for g value and reopen it by removing from CLOSED state and putting it into OPEN
        """
        # Initial start node
        start_node = Node(self.initial_state, None, self.INITIAL_G_VALUE,
                          self._find_minimum_heuristic_among_final_states(self.initial_state))
        # Open and closed lists
        open_list = [start_node]
        closed_list = []

        # Loop until open_list gets empty
        while open_list:
            current_node_index = Puzzle._find_minimum_f_valued_node(open_list)
            current_node = open_list.pop(current_node_index)

            # If it does not exist in closed_list, then put it there
            if not Puzzle._check_is_node_in_node_list(current_node.state, closed_list)[0]:
                closed_list.append(current_node)

            # If one of the final nodes is reached, then return solution
            if Puzzle._check_is_node_in_target_state_list(current_node.state, self.final_states):
                solution_path_to_initial_node = Puzzle._get_solution_path(current_node)
                return True, solution_path_to_initial_node
            else:
                # Step g value since we cannot find final node and need to apply one more iteration
                current_g_value = current_node.g_value + 1
                # Expand children nodes
                expanded_children = Puzzle._expand_node(current_node, self.block_count,
                                                        self.row_count, self.column_count)

                # Iterate over each children
                for child_state in expanded_children:
                    is_in_open_list, open_node = Puzzle._check_is_node_in_node_list(child_state, open_list)
                    is_in_closed_list, closed_node = Puzzle._check_is_node_in_node_list(child_state, closed_list)

                    if not is_in_open_list and not is_in_closed_list:
                        open_list.append(
                            Node(child_state, current_node, current_g_value,
                                 self._find_minimum_heuristic_among_final_states(child_state) + current_g_value)
                        )
                    else:
                        if is_in_open_list:
                            if open_node.g_value > current_g_value:
                                Puzzle._update_node(open_node, current_node, current_g_value)
                        elif is_in_closed_list:
                            if closed_node.g_value > current_g_value:
                                Puzzle._update_node(closed_node, current_node, current_g_value)
                                closed_list.remove(closed_node)
                                open_list.append(closed_node)
                        else:
                            print("Error: A node should not be found in both open and closed list")

        # If this point is reached, then return None representing FAILURE
        return False, None

    def _find_minimum_heuristic_among_final_states(self, state: List[List[int]]) -> int:
        """
        Minimum heuristic finding procedure among final states where the minimum distance of the current state
        to all final states are computed with respect to assigned heuristic function
        """
        heuristic_value_list = []
        for final_state in self.final_states:
            heuristic_value_list.append(self.heuristic_function(state, final_state))
        return min(heuristic_value_list)

    @staticmethod
    def _find_minimum_f_valued_node(open_list: List[Node]) -> int:
        """
        Finding minimum f-valued state in open states
        """
        minimum_index = 0
        minimum_f_value = open_list[0].f_value
        for index, open_node_from_list in enumerate(open_list):
            if open_node_from_list.f_value < minimum_f_value:
                minimum_index = index
                minimum_f_value = open_node_from_list.f_value
        return minimum_index

    @staticmethod
    def _check_is_node_in_node_list(state: List[List[int]], closed_state_list: List[Node])\
            -> Union[Tuple[bool, Node], Tuple[bool, None]]:
        """
        Check whether the given node is in the closed states
        """
        for closed_node in closed_state_list:
            if state == closed_node.state:
                return True, closed_node
        return False, None

    @staticmethod
    def _check_is_node_in_target_state_list(state: List[List[int]], target_state_list: List[List[List[int]]]) -> bool:
        """
        Check whether the given node is in the final state list
        """
        for target_state in target_state_list:
            if state == target_state:
                return True
        return False

    @staticmethod
    def _expand_node(node_to_expand: Node, pieces: int, row_count: int, column_count: int) -> List[List[List[int]]]:
        """
        Expand the given node by applying state transitions
        """
        current_state = node_to_expand.state
        children = []
        for block_to_slide in range(1, pieces + 1):
            # Functions to be applied where all the direction of sliding exist
            functions_to_be_applied = [st.slide_block_up, st.slide_block_down,
                                       st.slide_block_left, st.slide_block_right]
            for function in functions_to_be_applied:
                expanded_node = function(current_state, row_count, column_count, block_to_slide)
                if expanded_node is not None:
                    children.append(expanded_node)
        return children

    @staticmethod
    def _update_node(node_to_be_updated: Node, parent_node: Node, current_g_value: int):
        """
        Updating the given solution by changing its g value, parent node and f value
        """
        g_value_difference = node_to_be_updated.g_value - current_g_value
        node_to_be_updated.parent = parent_node
        node_to_be_updated.g_value = current_g_value
        node_to_be_updated.f_value -= g_value_difference

    @staticmethod
    def _get_solution_path(final_node: Node) -> List[Node]:
        """
        Finding solution path via iterating parents until the start node
        """
        solution_path_to_initial_node = []
        while final_node.parent is not None:
            solution_path_to_initial_node.insert(0, final_node)
            final_node = final_node.parent
        solution_path_to_initial_node.insert(0, final_node)
        return solution_path_to_initial_node


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
    solution_exists, solution_path = puzzle.solve()
    if solution_exists:
        for node in solution_path:
            for row in node.state:
                print(row)
            print()
    else:
        print("Solution does not exist.")