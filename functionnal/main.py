from pandas import read_csv
from sklearn import preprocessing
from model.preprocess_coins import execute
from model.env_class import BitcoinTradingEnv
from model.stock_trad_env_class import StockTradingEnvironment
from model.personnal_env import CustomEnv
import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines.common import vec_env
from stable_baselines import PPO2



df = execute('./Binance_BTCUSDT_minute.csv')
print('-----------------')
print(df.loc[5: 10].columns)
#df = read_csv('./Binance_BTCUSDT_minute.csv')
#env = vec_env.DummyVecEnv([lambda: StockTradingEnvironment(df)])
#env =  vec_env.DummyVecEnv([lambda: BitcoinTradingEnv(df, commission=0, serial=False)])
env = make_vec_env(lambda: CustomEnv(df, 10000, 50000, 0.2, 500))

model = PPO2("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)


# Enjoy trained agent
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
