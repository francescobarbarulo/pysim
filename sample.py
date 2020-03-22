from core.simulator import Simulator

# import your own modules, for instance
from examples.Sample.sampleModule import SampleModule


def main():
    # create a new simulator
    sim = Simulator()

    # register your module
    sim.register(SampleModule("sample"))

    # run the simulator
    sim.run()


if __name__ == '__main__':
    main()
