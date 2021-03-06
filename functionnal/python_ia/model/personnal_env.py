from traceback import print_tb
import sys
import gym
import numpy as np
from gym import spaces


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    HODL = 0
    BUY = 1
    SELL = 2

    def __init__(self, df, initial_balance, n_iteration, comission, start_at=0):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.done = 0
        self.binance_capital = 0
        self.current_iteration = 0
        self.current_balance = initial_balance
        self.start_index = start_at
        self.last_action = -1
        self.max_iteration = n_iteration
        self.current_held = 0
        self.df = df
        self.take_action = 0
        self.current_index = start_at
        self.buy_at = df.iloc[self.current_index]['close']
        self.sell_at = df.iloc[self.current_index]['close']
        self.portion = 0

        self.portion_to_binance = 0
        

        number_of_actions = 3  # Buy, Sell, Hodl

        self.current_price = df.iloc[self.current_index]['close']
        self.action_space = spaces.Box(low=np.array(
            [0, 0]), high=np.array([3, 1]))  # amount

        self.initial_balance = initial_balance
        self.n_iteration = n_iteration
        self.comission = comission
        self.multiplier = 1 - self.comission
        # Example for using image as input:
        #self.observation_space = spaces.Box(low=np.full((8,), -np.inf), high=np.full((8,), np.inf), dtype=np.float32)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(8, 501), dtype=np.float32)

    def _next_observation(self):
        obs = np.array([
            self.df.loc[self.current_index: self.current_index + 500, 'open'],
            self.df.loc[self.current_index: self.current_index + 500, 'high'],
            self.df.loc[self.current_index: self.current_index + 500, 'low'],
            self.df.loc[self.current_index: self.current_index + 500, 'close'],
            self.df.loc[self.current_index: self.current_index + 500, 'Volume BTC'],
            self.df.loc[self.current_index: self.current_index + 500, 'Volume USDT'],
            self.df.loc[self.current_index: self.current_index + 500, 'day_of_the_week'],
            self.df.loc[self.current_index: self.current_index + 500, 'hour_of_the_day']
            # self.current_balance,
            # self.current_held,
            # self.current_price
        ])
        return obs

    def reset(self):
        self.current_index = self.start_index
        self.current_balance = self.initial_balance
        self.current_price = self.df.iloc[self.current_index]['close']
        observation = self._next_observation()
        return observation  # reward, done, info can't be included

    def step(self, action):
        self.take_action = action
        self.current_price = self.df.iloc[self.current_index - 1]['close']
        reward = 0
        done = bool(self.current_index >=
                    self.df.shape[0] or self.current_iteration >= self.max_iteration)

        self.done = done
        old_balance = self.current_balance

        action_type = action[0]
        amount = action[1]  # Percentage
        self.portion = amount * self.current_balance

        if action_type < 1:  # HODL
            self.last_action = "HOLD"
            reward = self.buy_at - (self.current_price * self.multiplier)
            
        elif action_type < 2:  # BUY
            self.buy_at = self.current_price
            if self.current_balance < 1:
                reward = - (self.initial_balance / 2)
            else:
                self.last_action = "BUY"
                buy = (amount * self.current_balance) / self.current_price
                self.current_held += buy * self.multiplier
                self.current_balance -= (amount * self.current_balance)
                self.portion_to_binance = self.current_price * amount * (1 - self.multiplier)
                self.binance_capital += self.current_price * amount * (1 - self.multiplier)
                reward = self.sell_at * self.multiplier - self.current_price
        elif action_type < 3:  # SELL
            can_sell = self.current_held * self.current_price
            selling = self.current_held * amount
            benef = selling * self.current_price
            self.last_action = "SELL"
            self.current_held -= selling
            self.current_balance += benef * self.multiplier
            self.binance_capital += benef * (1 - self.multiplier)
            self.sell_at = self.current_price
            reward = self.current_price * self.multiplier - self.buy_at
            self.portion_to_binance = benef * (1 - self.multiplier)

        self.current_index -= 1
        self.current_iteration += 0 

        return self._next_observation(), reward, done, {}

    def render(self, mode='human'):
        if self.last_action == 'HOLD':
            return
        print(f'-----------------------------------------------')
        print(f'multiplier = {self.multiplier}')
        print(f'step {self.current_iteration} / {self.max_iteration}')
        print(f'Bot Choose to {self.last_action}')
        print(f'Initial Balance {self.initial_balance}')
        print(f'Current Balance {self.current_balance}')
        print(f'Current Price: {self.current_price} USDT')
        print(f'Current Hodl: {self.current_held} BTC')
        print(f'portion choosen: {self.portion}')
        print(f'current portion {self.portion_to_binance}')
        print(f'Les poches de binances {self.binance_capital}')

        print(
            f'Profit: {(self.current_balance + (self.current_held * self.current_price))- self.initial_balance}')
        #print(f'Taken action: {self.take_action}')

    def close(self):
        print('Simulation done')
        print(
            f'went from {self.initial_balance} to {(self.current_balance + self.current_held * self.current_price)}')
        profit = (self.current_balance + self.current_held *
                  self.current_price) - self.initial_balance
        print(f'Profit is {profit}')
        sys.exit(0)
