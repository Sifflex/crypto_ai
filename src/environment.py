import numpy as np
import pandas as pd

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

tf.compat.v1.enable_v2_behavior()


class CryptoTradingEnv(py_environment.PyEnvironment):
    def __init__(self, df, fee = 0.001, initial_balance = 100, look_back_window = 90):
        # Initialize the action spec and observation spec,
        #  the two main components of agent will need to navigate the environment
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(3,), dtype=np.int32, minimum=0, maximum=10, name='action'
        )

        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1,4,90), dtype=np.float32, minimum=0, name='observation'
        )
        
        self._state = np.zeros(
            (4,5,40), dtype=np.float32
        )

        # Parameters specific to the environment
        self._episode_ended = False
        self.initial_balance = initial_balance
        self.last_balance = initial_balance

        # self.wallet[0] is fiat balance
        self.wallet = { 'USDT' : self.initial_balance } 

        # How far back our agent will observe to make it's prediction
        self.look_back_window = look_back_window

        # Trading fees
        self.fee = fee

        # Used for the rendering and visualization
        self.visual = None

        # Set the initial step to the look back window so that our agent will have data to view on it's first step
        self.current_step = self.look_back_window

        # Store the trades made
        self.moves = { 'USDT' : [] }

        self.df = df

        self.crypto_pairs = self.df.index.get_level_values(0).unique()
        self.intervals = self.df.index.get_level_values(1).unique()

        self.size_df = len(self.crypto_pairs) * len(self.intervals)

        for cp in self.crypto_pairs:
            print("loading " + cp)
            self.moves[cp].append([])
            self.wallet[cp].append(0.0)

    def reset(self):
        self.initial_time_step = ts.restart(self._state)
        self.wallet = [self.initial_balance]
        for _ in self.size_df:
            self.wallet.append(0.0)
        self.current_step = self.look_back_window
        return ts.restart(self._state)

    def step(self, action):
        # Apply action and return a new time_step
        slicing_start = self.current_step - (self.look_back_window * 60000)
        slicing_end = self.current_step
        data = self.df[:, :, slicing_start:slicing_end]

        self._state = np.array(data)

        coin = action[0]
        action_type = action[1]
        amount = action[2] / 10.0

        reward = self.evaluate()

        # TODO: Change to total portofolio value 
        # If we lost 99% of our wallet that may be a good time to stop
        if self.wallet[0] < 0.01 * self.initial_balance:
            self._episode_ended = True
            return ts.termination(self._state, reward)

        if action_type is 0:
            # We're buying
            current_price = data.loc[[coin], :, :]["close"][-1]
            # This formulation works when buying x percents of our current fiat money
            buying_amount = self.wallet[0] * amount
            self.wallet['USDT'] = self.wallet['USDT'] - buying_amount
            self.wallet[coin] = self.wallet[coin] + buying_amount / current_price
            self.moves[coin].append(('buy', self.current_step, current_price))


        elif action_type is 1:
            # We're selling
            current_price = data.loc[[coin], :, :]["close"][-1]
            selling_amount = amount * self.wallet[coin]
            self.wallet[coin] = self.wallet[coin] - selling_amount
            self.wallet['USDT'] = self.wallet['USDT'] + selling_amount * current_price
            self.moves[coin].append(('sell', self.current_step, current_price))

        self.current_step += 60000
        return ts.transition(self._state, reward, 1.0)

    def evaluate(self):
        # Calculating current balance
        current_balance = 0
        for coin in self.wallet:
            current_balance += self.wallet[coin] * self.df.loc[coin, :, self.current_step]["close"][-1]
        
        reward = 0
        
        # TODO: Improve the reward calculation system
        # Calculating the reward, this part is (for now) completly subjective and subject to changes
        reward += (-1 if current_balance < self.last_balance else 1) * self.last_balance / current_balance
        reward += (-1 if current_balance < self.initial_balance else 1) * self.initial_balance / current_balance
    
        return reward