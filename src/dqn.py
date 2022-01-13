import copy
import numpy as np
import pandas as pd
import chainer
import chainer.functions as F
import chainer.links as L

class Q_Network(chainer.Chain):
    def __init__(self, input_size, hidden_size, output_size):
        super(Q_Network, self).__init__(
        fc1 = L.Linear(input_size, hidden_size),
        fc2 = L.Linear(hidden_size, hidden_size),
        fc3 = L.Linear(hidden_size, output_size)
    )

    def __call__(self, x):
        h = F.relu(self.fc1(x))
        h = F.relu(self.fc2(h))
        y = self.fc3(h)
        return y

    def reset(self):
        self.zerograds()

def train_dqn(env):
    Q = Q_Network(input_size=env.lookback_window + 1, hidden_size=100, output_size=3)
    Q_ast = copy.deepcopy(Q)
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(Q)

    epoch_num = 50
    step_max = len(env.df.shape(0)) - 1
    memory_size = 200
    batch_size = 20
    epsilon = 1.0
    epsilon_decrease = 1e-3
    epsilon_min = 0.1
    start_reduce_epsilon = 200
    train_freq = 10
    update_q_freq = 20
    gamma = 0.97
    show_log_freq = 5

    memory = []
    total_step = 0
    total_rewards = []
    total_losses = []