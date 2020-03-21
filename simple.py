"""
    *** Simple example ***
    This simulation implements an echo-reply interaction between two modules.
"""

from modules.simpleModule import SimpleModule
from core.simulator import sim


def main():
    sim.add_module(SimpleModule("s1"), SimpleModule("s2"))

    sim.run()


if __name__ == '__main__':
    main()

