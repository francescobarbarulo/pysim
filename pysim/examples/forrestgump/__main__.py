from pysim.core.experiment import ex
from pysim.core.simulator import Simulator
from pysim.core.modules.mobileModule import MobileModule


@ex.automain
def main():
    sim = Simulator()

    sim.register_module(MobileModule, 'Forrest Gump')

    sim.run()
