from tictoc import TicTocModule
from core.simulator import Simulator
from core import sim


def main():

    sim.sim = Simulator()

    sim.sim.add_module(TicTocModule("s1"))
    sim.sim.add_module(TicTocModule("s2"))

    sim.sim.run()


if __name__ == '__main__':
    main()

