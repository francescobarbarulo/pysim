"""
    *** tictoc example ***
    This simulation implements a tic-toc interaction between two modules.
    Module "tic" starts the loop interaction with "toc".
"""

from pysim.examples.tictoc.modules.ticModule import TicModule
from pysim.examples.tictoc.modules.tocModule import TocModule
from pysim.core.simulator import Simulator


def main():
    sim = Simulator()

    sim.register_module(TicModule("tic"))
    sim.register_module(TocModule("toc"))

    sim.run()


if __name__ == '__main__':
    main()

