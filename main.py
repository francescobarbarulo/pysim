from examples.simpleModule import SimpleModule
from examples.tictoc import TicTocModule
from core.simulator import sim


def main():

    sim.add_module(TicTocModule("s1"))
    sim.add_module(TicTocModule("s2"))

    sim.run()


if __name__ == '__main__':
    main()

