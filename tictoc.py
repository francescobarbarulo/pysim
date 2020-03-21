"""
    *** TicToc example ***
    This simulation implements a tic-toc interaction between two modules.
    Module s1 starts the interaction with s2 and they continue forever.
"""

from modules.ticTocModule import TicTocModule
from core.simulator import Simulator


def main():
    sim = Simulator()
    ''' 
        Add modules here:
        - in a single statement like in the example;
        - in more statements:
            sim.add_module(TicTocModule("s1"))
            sim.add_module(TicTocModule("s2"))

    '''
    sim.add_module(TicTocModule("s1"), TicTocModule("s2"))

    sim.run()


if __name__ == '__main__':
    main()

