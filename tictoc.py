"""
    *** TicToc example ***
    This simulation implements a tic-toc interaction between two modules.
    Module "tic" starts the loop interaction with "toc".
"""

from examples.TicToc.ticModule import TicModule
from examples.TicToc.tocModule import TocModule
from pysim.simulator import Simulator


def main():
    sim = Simulator()

    sim.register_module(TicModule("tic"))
    sim.register_module(TocModule("toc"))

    sim.run()


if __name__ == '__main__':
    main()

