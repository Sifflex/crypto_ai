import tensorflow as tf
import numpy as np
import pandas as pd

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

from Visualization import TradingGraph as tg

tf.compat.v1.enable_v2_behavior()

class CryptoTradingEnv(py_environment.PyEnvironment):
    def __init__(self, fee = 0.001, initial_balance = 100 look_back_window = 100, df):
        # Initialize the action spec and observation spec,
        #  the two main components of agent will need to navigate the environment
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(3,), dtype=np.int32, minimum=0, maximum=10, name='action'
        )
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(4,5,40), dtype=np.float32, minimum=0, name='observation')
            self._state = np.zeros((4,5,40), dtype=np.float32
        )

        # Parameters specific to the environment
        self._episode_ended = False
        self.initial_balance = initial_balance

        # self.wallet[0] is fiat balance
        self.wallet = [self.initial_balance]

        # How far back our agent will observe to make it's prediction
        self.look_back_window = look_back_window

        # Trading fees
        self.fee = fee

        # Used for the rendering and visualization
        self.visual = None

        # Set the initial step to the look back window so that our agent will have data to view on it's first step
        self.current_step = self.look_back_window

        # Store the trades made
        self.moves = []

        self.df = df

        """
            Iterate over the crypto pairs and:
                - append and empty list for each coin to store the trades
                - inititalize each coin in our wallet to 0.0
        """
        self.crypto_pairs = self.df.index.get_level_values(0).unique()
        self.intervals = self.df.index.get_level_values(1).unique()

        self.size_df = len(crypto_pairs) * len(intervals)

        for cp in crypto_pairs:
            for i in intervals:
                print("loading " + i + " " + cp)
                self.moves.append([])
                self.wallet.append(0.0)

    def reset(self):
    """Returns initial_time_step"""
        self.initial_time_step = ts.restart(self._state)
        self.wallet = [self.initial_balance]
        for _ in self.size_df:
            self.wallet.append(0.0)
        self.current_step = self.look_back_window
        return ts.restart(self._state)

    def step(self, action)
        # Apply action and return a new time_step
        slicing_start = self.current_step - (self.look_back_window * 60000)
        slicing_end = self.current_step
        data = self.df[:, :, slicing_start:slicing_end]

        self._state = np.array(data)

        coin = action[0]
        action_type = action[1]
        amount = action[2] / 10.0

        reward = 0

        # If we lost 99% of our wallet that may be a good time to stop
        if self.wallet[0] < 0.01 * self.initial_balance:
            self._episode_ended = True
            return ts.termination(self._state, reward)

        # We're buying
        if action_type is 0:
            current_price 
