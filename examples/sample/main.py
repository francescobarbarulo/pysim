from pysim.core.simulator import Simulator
from pysim.core.experiment import ex

# import your own modules, for instance
from modules import SampleModule


@ex.automain
def main():
    # create a new simulator
    sim = Simulator()

    # register your module
    sim.register_module(create_module=SampleModule, name='sample')

    # run the simulator
    sim.run()
