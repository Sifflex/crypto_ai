"""Simulation module"""

import pandas as pd
from dataset import load_dataset

from simulations.internal_state import InternalState
from simulations.simulation_config import SimulationConfig


def simulate():
    """Run a simulation and return results"""

    simulation_config = SimulationConfig()
    internal_state = InternalState()
    df = load_dataset()

    interval = 15 * 60 * 1000
    time = 1627046100000
    start_time = time - (interval * 9)

    fifteen_min = df.loc[:, "15MIN", start_time:time]
    print(fifteen_min)
    shapes = fifteen_min.groupby("symbol").size().to_numpy()
    # data = fifteen_min.to_numpy().reshape(shapes)
    # print(data.shape)
