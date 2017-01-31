#!/usr/bin/env python
"""
A basic adaptive bot. This is part of the second worksheet.

"""

from api import State, util
import random, os

from sklearn.externals import joblib

DEFAULT_MODEL = os.path.dirname(os.path.realpath(__file__)) + '/model.pkl'

class Bot:

    __max_depth = -1
    __randomize = True

    __model = None

    def __init__(self, randomize=True, depth=4, model_file=DEFAULT_MODEL):

        print(model_file)
        self.__randomize = randomize
        self.__max_depth = depth

        # Load the model
        self.__model = joblib.load(model_file)

    def get_move(self, state):

        val, move = self.value(state)

        return move

    def value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0):
        """
        Return the value of this state and the associated move
        :param state:
        :param alpha: The highest score that the maximizing player can guarantee given current knowledge
        :param beta: The lowest score that the minimizing player can guarantee given current knowledge
        :param depth: How deep we are in the tree
        :return: val, move: the value of the state, and the best move.
        """
        if state.finished():
            return (1.0, None) if state.winner() == 1 else (-1.0, None)

        if depth == self.__max_depth:
            return self.heuristic(state), None

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            next_state = state.next(move)
            value, m = self.value(next_state, alpha, beta, depth + 1)

            if maximizing(state):
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
            if alpha > beta or beta < alpha:
                break

        return best_value, best_move

    def heuristic(self, state):
        # Convert the state to a feature vector
        feature_vector = [four_dimension_features(state)]

        # These are the classes: ('won', 'lost')
        classes = list(self.__model.classes_)

        # Ask the model for a prediction
        # This returns a probability for each class
        # print('{}'.format(feature_vector[0]))
        prob = self.__model.predict_proba(feature_vector)[0]
        # print('{} {} {}'.format(classes, prob, util.ratio_ships(state, 1)))

        # Weigh the win/loss outcomes (-1 and 1) by their probabilities
        res = -1.0 * prob[classes.index('lost')] + 1.0 * prob[classes.index('won')]
        # print(res)

        return res

def maximizing(state):
    """
    Whether we're the maximizing player (1) or the minimizing player (2).
    :param state:
    :return:
    """
    return state.whose_turn() == 1


def four_dimension_features(state):
    # type: (State) -> tuple[float, ...]
    """
    Extract features from this state. Remember that every feature vector returned should have the same length.

    :param state: A state to be converted to a feature vector
    :return: A tuple of floats: a feature vector representing this state.
    """

    # Find out which player we are
    my_id = state.whose_turn()
    other_id = util.other(my_id)

    # How many ships does p1 have in garrisons?
    p1_garrisons = util.player_garissons(state, my_id)
    # How many ships does p2 have in garrisons?
    p2_garrisons = util.player_garissons(state, other_id)


    # How many ships does p1 have in fleets?
    p1_fleets = util.player_fleets(state, my_id)
    # How many ships does p2 have in fleets?
    p2_fleets = util.player_fleets(state, other_id)

    return p1_garrisons, p2_garrisons, p1_fleets, p2_fleets

def test_feature(state):
    # type: (State) -> tuple[float, ...]

    # Find out which player we are
    my_id = state.whose_turn()
    other_id = util.other(my_id)

    p1_avg_growth = util.average_plaet_growth_rate(state, my_id)
    p2_avg_growth = util.average_plaet_growth_rate(state, other_id)

    p1_ratio_ship = util.ratio_ships(state, my_id)
    p2_ratio_ship = util.ratio_ships(state, other_id)

    # How many ships does p1 have in fleets?
    p1_fleets = util.player_fleets(state, my_id)
    # How many ships does p2 have in fleets?
    p2_fleets = util.player_fleets(state, other_id)

    return p1_avg_growth, p2_avg_growth, p1_ratio_ship, p2_ratio_ship, p1_fleets, p2_fleets

