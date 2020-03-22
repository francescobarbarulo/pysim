"""
    *** TicToc example ***
    This simulation implements a tic-toc interaction between two modules.
    Module "tic" starts the interaction with "toc" and they continue forever.
    Stop it issuing Ctrl+C
"""

from examples.TicToc.ticModule import TicModule
from examples.TicToc.tocModule import TocModule
from core.simulator import Simulator


def main():
    sim = Simulator()

    sim.register(TicModule("tic"), TocModule("toc"))

    sim.run()


if __name__ == '__main__':
    main()

