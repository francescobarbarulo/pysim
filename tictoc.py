"""
    *** TicToc example ***
    This simulation implements a tic-toc interaction between two modules.
    Module s1 starts the interaction with s2 and they continue forever.
"""

from modules.ticTocModule import TicTocModule
from core.simulator import sim


def main():
    sim.add_module(TicTocModule("s1"), TicTocModule("s2"))

    sim.run()


if __name__ == '__main__':
    main()

