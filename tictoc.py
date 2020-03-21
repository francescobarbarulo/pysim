"""
    *** TicToc example ***
    This simulation implements a tic-toc interaction between two examples.
    Module s1 starts the interaction with s2 and they continue forever.
"""

from examples.TicToc.ticModule import TicModule
from examples.TicToc.tocModule import TocModule
from core.simulator import Simulator


def main():
    sim = Simulator()
    ''' 
        Add examples here:
        - in a single statement like in the example;
        - in more statements:
            sim.add_module(TicTocModule("s1"))
            sim.add_module(TicTocModule("s2"))

    '''
    sim.add_module(TicModule("tic"), TocModule("toc"))

    sim.run()


if __name__ == '__main__':
    main()

