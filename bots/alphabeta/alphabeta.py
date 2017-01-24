#!/usr/bin/env python
"""


"""

from api import State, util
import random

class Bot:

    __max_depth = -1
    __randomize = True
    __my_id = 0

    def __init__(self, randomize=True, depth=4):
        self.__randomize = randomize
        self.__max_depth = depth

    def get_move(self, state):
        # Find out which player we are
        self.__my_id = state.whose_turn()

        val, move = self.value(state)

        return move # to do nothing, return None

    def value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0):
        """
        Return the value of this state and the associated move
        :param State state:
        :param float alpha: The highest score that the maximizing player can guarantee given current knowledge
        :param float beta: The lowest score that the minimizing player can guarantee given current knowledge
        :param int depth: How deep we are in the tree
        :return val, move: the value of the state, and the best move.
        """
        if state.finished():
            return (1.0, None) if state.winner() == 1 else (-1.0, None)

        if depth == self.__max_depth:
            return heuristic(state)

        best_value = float('-inf') if maximizing(state, self.__my_id) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            next_state = state.next(move)
            value, _ = ???

            if maximizing(state, self.__my_id):
                if value > best_value:
                    best_value = value
                    best_move = move
                    alpha = best_value
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                    beta = best_value

            # Prune the search tree
            # We know this state will never be chosen, so we stop evaluating its children
            if ???:
                break

        return best_value, best_move

def maximizing(state, my_id):
    """
    Whether we're the maximizing player (1) or the minimizing player (2).

    :param state:
    :return:
    """
    return state.whose_turn() == my_id

def heuristic(state):
    return util.ratio_ships(state, 1) * 2.0 - 1.0, None
