#!/usr/bin/python3.7
import warnings
warnings.filterwarnings("ignore")
import sys
from operator import mod
from numpy import float32
from pandas import read_csv
from sklearn import preprocessing
from model.preprocess_coins import execute
from model.env_class import BitcoinTradingEnv
from model.stock_trad_env_class import StockTradingEnvironment
from model.personnal_env import CustomEnv
import gym
import numpy as np
import pickle

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines.common import vec_env
from stable_baselines import PPO2

#open high low close volumebtc volumeusdt dayweek hoursday

all_array = []

for i in range(len(sys.argv)):
    if i == 0:
        continue
    all_array.append(float32(sys.argv[i]))

print(all_array)

model = PPO2.load('./model.tradebot')

action, _states = model.predict(np.array([all_array]))

print(action)
print(_states)

