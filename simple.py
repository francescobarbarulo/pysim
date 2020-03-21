"""
    *** Simple example ***
    This simulation implements an echo-reply interaction between two modules.
"""

from modules.simpleModule import SimpleModule
from core.simulator import Simulator


def main():
    sim = Simulator()
    ''' 
        Add modules here:
        - in a single statement like in the example;
        - in more statements:
            sim.add_module(SimpleModule("s1"))
            sim.add_module(SimpleModule("s2"))
    
    '''
    sim.add_module(SimpleModule("s1"), SimpleModule("s2"))

    sim.run()


if __name__ == '__main__':
    main()

