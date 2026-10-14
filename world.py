#!/usr/bin/env python
# Olivier Georgeon, 2021.
# This code is used to teach Developmental AI.

# TODO: Uncomment the environment to test your agent in one of these more complex environment
from turtlepy_enacter import TurtlePyEnacter

#from PetitCatEnacter import PetitCatEnacter
#from turtlesim_enacter import TurtleSimEnacter # requires ROS


import random
class Agent2:
    def __init__(self, _valences):
        """ Creating our agent """
        self._valences = _valences
        self._action = None
        self._predicted_outcome = None
        self._positive_action = None
        self._known_outcomes = {}
        self.cpt = 0

    def action(self, _outcome):
        """ tracing the previous cycle """
        if self._action is not None:
            print(f"Action: {self._action}, Prediction: {self._predicted_outcome}, Outcome: {_outcome}, "
                  f"Prediction: {self._predicted_outcome == _outcome}, Valence: {self._valences[self._action][_outcome]}")

        """ Computing the next action to enact """
        # TODO: Implement the agent's decision mechanism

        if self._positive_action is None:
            if self._action is None:
                self._action = 0

        # outcome de l'action précédente
        self._known_outcomes[self._action] = _outcome

        #regarde si la valence est positif
        if self._valences[self._action][_outcome] == 1:
            self._positive_action = self._action
            self.cpt += 1
        else:
            self.cpt = 0

        #calcul de la prochaine action

        if self._positive_action is None:
            #pas d'action positive exploré
            if self._action is None:
                self._action = 0
            else:
                self._action = 1 - self._action
        elif self.cpt < 4:
            #préfère les actions positives
            self._action = self._positive_action
        else:
            #essayer d'autre actions
            self._action = 1 - self._positive_action
            self.cpt = 0


        #anticipation
        self._predicted_outcome = self._known_outcomes.get(
            self._action, None
        )

        return self._action


class Agent:
    def __init__(self, _valence_table):
        """ Creating our agent """
        self._valence_table = _valence_table
        self._action = None
        self._anticipated_outcome = None

    def action(self, _outcome):
        """ tracing the previous cycle """
        if self._action is not None:
            print("Action: " + str(self._action) +
                  ", Anticipation: " + str(self._anticipated_outcome) +
                  ", Outcome: " + str(_outcome) +
                  ", Satisfaction: (anticipation: " + str(self._anticipated_outcome == _outcome) +
                  ", valence: " + str(self._valence_table[self._action][_outcome]) + ")")

        """ Computing the next action to enact """
        # TODO: Implement the agent's decision mechanism
        self._action = 0
        # TODO: Implement the agent's anticipation mechanism
        self._anticipated_outcome = 0
        return self._action


class Environment1:
    """ In Environment 1, action 0 yields outcome 0, action 1 yields outcome 1 """
    def outcome(self, _action):
        # return int(input("entre 0 1 ou 2"))
        if _action == 0:
            return 0
        else:
            return 1


class Environment2:
    """ In Environment 2, action 0 yields outcome 1, action 1 yields outcome 0 """
    def outcome(self, _action):
        if _action == 0:
            return 1
        else:
            return 0


class Environment3:
    """ Environment 3 yields outcome 1 only when the agent alternates actions 0 and 1 """
    def __init__(self):
        """ Initializing Environment3 """
        self.previous_action = 0

    def outcome(self, _action):
        _outcome = 1
        if _action == self.previous_action:
            _outcome = 0
        self.previous_action = _action
        return _outcome


# TODO Define the valance of interactions (action, outcome)
valences = [[-1, 1], [-1, 1]]
# valences = [[1, -1], [1, -1]]
# TODO Choose an agent
a = Agent2(valences)
# TODO Choose an environment
#e = Environment1()
# e = Environment2()
# e = Environment3()
e = TurtlePyEnacter()
# e = TurtleSimEnacter()

if __name__ == '__main__':
    """ The main loop controlling the interaction of the agent with the environment """
    outcome = 0
    for i in range(20):
        action = a.action(outcome)
        outcome = e.outcome(action)
