from pysim.core.simulator import Simulator

# import your own modules, for instance
from pysim.examples.sample.modules.sampleModule import SampleModule


def main():
    # create a new simulator
    sim = Simulator()

    # register your module
    sim.register_module(SampleModule, 'sample')

    # run the simulator
    sim.run()


if __name__ == '__main__':
    main()
