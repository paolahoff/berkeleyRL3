# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util
from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0

        states = self.mdp.getStates()
        updated_values = []
        for _ in range(self.iterations):
            updated_values = self.values.copy()
            for state in states:
                # Doesn't get reward for terminal states
                if self.mdp.isTerminal(state):
                    continue
                updated_values[state] = self.computeQValueFromValues(state, self.getPolicy(state))
            self.values = updated_values.copy()


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        next_states = self.mdp.getTransitionStatesAndProbs(state, action)
        action_value = 0
        for next_state, probability in next_states:
            # Bellman equation
            action_value += probability * (self.mdp.getReward(state, action, next_state) + self.discount * self.values[next_state])
        return action_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        # If state is terminal, return None
        if self.mdp.isTerminal(state):
            return None
        # Compute the Q value of all possible actions given an actual state, then return the action with the maximum value computed
        possible_actions = self.mdp.getPossibleActions(state)
        action_values = []
        for action in possible_actions:
            action_values.append(self.computeQValueFromValues(state, action))
        max_value = max(action_values)
        max_value_index = action_values.index(max_value)
        return possible_actions[max_value_index]
        
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
