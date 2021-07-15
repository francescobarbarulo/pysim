"""
    *** tictoc example ***
    This simulation implements a tic-toc interaction between two modules.
    Module "tic" starts the loop interaction with "toc".
"""

from pysim.core.simulator import Simulator
from pysim.core.experiment import ex
from modules import TicModule, TocModule


@ex.automain
def main():
    sim: Simulator = Simulator()

    sim.register_module(create_module=TicModule, name='tic')
    sim.register_module(create_module=TocModule, name='toc')

    sim.run()
