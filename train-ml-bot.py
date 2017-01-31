"""
Train a machine learning model for the classifier bot. We create a player, and watch it play games against itself.
Every observed state is converted to a feature vector and labeled with the eventual outcome
(-1.0: player 2 won, 1.0: player 1 won)

This is part of the second worksheet.
"""
from api import State, util

# This package contains various machine learning algorithms
import sys
import sklearn, inspect, os
import sklearn.linear_model
from sklearn.externals import joblib

from bots.rand import rand
from bots.alphabeta import alphabeta
from bots.ml import ml

from bots.ml.ml import four_dimension_features

import matplotlib.pyplot as plt

# How many games to play
GAMES = 1000
# Number of planets in the field
NUM_PLANETS = 6
# Maximum number of turns to play
NUM_TURNS = 100
# Train for symmetric start states
SYM = True

# The player we'll observe
player = rand.Bot()
# player = alphabeta.Bot()

data = []
target = []

for g in range(GAMES):

    state, id = State.generate(NUM_PLANETS, symmetric=SYM)

    state_vectors = []
    i = 0
    while not state.finished() and i <= NUM_TURNS:
        state_vectors.append(four_dimension_features(state))

        move = player.get_move(state)
        state = state.next(move)

        i += 1

    winner = state.winner()

    for state_vector in state_vectors:
        data.append(state_vector)

        if winner == 1:
            result = 'won'
        elif winner == 2:
            result = 'lost'
        else:
            result = 'draw'
        target.append(result)

    sys.stdout.write(".")
    sys.stdout.flush()
    if g % (GAMES/10) == 0:
        print("")
        print('game {} finished ({}%)'.format(g, (g/float(GAMES)*100)))

# Train a logistic regression model
learner = sklearn.linear_model.LogisticRegression()
model = learner.fit(data, target)

# Check for class imbalance
count = {}
for str in target:
    if str not in count:
        count[str] = 0
    count[str] += 1

print('instances per class: {}'.format(count))

# Store the model in the ml directory
classpath = inspect.getfile(player.__class__)
base = os.path.basename(classpath)
filename = './bots/ml/'+os.path.splitext(base)[0]+'-model.pkl'
joblib.dump(model, filename)

print('Done')




