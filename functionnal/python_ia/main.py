from operator import mod
from pandas import read_csv
from sklearn import preprocessing
from model.preprocess_coins import execute
from model.env_class import BitcoinTradingEnv
from model.stock_trad_env_class import StockTradingEnvironment
from model.personnal_env import CustomEnv
import gym


import pickle

from stable_baselines.common.policies import MlpPolicy, LstmPolicy, FeedForwardPolicy, register_policy
from stable_baselines.common import make_vec_env
from stable_baselines.common import vec_env
from stable_baselines import PPO2


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp)


df = execute('./Binance_BTCUSDT_minute.csv')
print('-----------------')
print(df.loc[5: 10].columns)
#df = read_csv('./Binance_BTCUSDT_minute.csv')
#env = vec_env.DummyVecEnv([lambda: StockTradingEnvironment(df)])
#env =  vec_env.DummyVecEnv([lambda: BitcoinTradingEnv(df, commission=0, serial=False)])
env = make_vec_env(lambda: CustomEnv(df, 10000, 500000, 0.1, 1240181 - 501))

all_args = dict(n_envs=4, n_nminibatches=1)
#(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, n_lstm=64, reuse=False, **_kwargs)
class CustomLSTMPolicy(LstmPolicy):
    def __init__(self, n_env, n_steps, n_batch, n_lstm=64, reuse=False, **_kwargs):
        super().__init__(n_env, n_steps, n_batch, n_lstm, reuse,
                         net_arch=[8, 'lstm', dict(vf=[5, 10], pi=[10])],
                         layer_norm=True, feature_extraction="mlp", **_kwargs)

# Custom MLP policy of three layers of size 128 each
class CustomPolicyMLP(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomPolicyMLP, self).__init__(*args, **kwargs,
                                           net_arch=[64, dict(pi=[256, 64, 128, 64, 256],
                                                          vf=[128, 128, 128])],
                                           feature_extraction="mlp")

# Register the policy, it will check that the name is not already taken
register_policy('CustomPolicy', CustomPolicyMLP)

model = PPO2('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=50000)

# Enjoy trained agent
dones = False
obs = env.reset()
i = 0
while not dones:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    i += 1
    if i % 1 == 0:
        env.render()

#final = model
#save_object(final, 'model.tradebot')
model.save('./model.tradebot')

print('Mercee pour les travaux')
