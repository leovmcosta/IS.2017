#!/usr/bin/env python
"""
MyBot - A simple strategy: Pick his strongest planet and attack a random enemy player or neutral planet
"""

# Import the API objects

import api.util as u

class Bot:

    def __init__(self):
        pass

    def get_move(self, state):

        # Find out which player we are
        my_id = state.whose_turn()

        # Our move: these will contain Planet objects
        source = None
        dest = None

        sources_strengths = []        # list containing our planets strengths
        dest_strength = -1 # destination score must end up as large as possible (start with low value)

        # Find my planets strengths
        for mine in state.planets(my_id):
            sources_strengths.append(state.garrison(mine))

        # Find what's the median strength
        mid = sorted(sources_strengths)[len(sources_strengths) // 2]

        # Find what's the planet with the median strength
        for mine in state.planets(my_id):
            if mid == state.garrison(mine):
                source = mine

        # Find the strongest enemy or neutral planet (larger number of ships).
        for his in (state.planets(u.other(my_id)) + state.planets(0)):
            strength = state.garrison(his)
            if strength > 1 and strength > dest_strength:
                dest_strength = strength
                dest = his

        if source is None or dest is None:
            return None

        return source.id(), dest.id()

