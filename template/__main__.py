from pysim.core.experiment import ex
from pysim.core.simulator import Simulator

from template.modules.myModule import MyModule


@ex.config
def config():
    pass


@ex.automain
def main():
    sim = Simulator()

    sim.register_module(MyModule, 'my-module')

    sim.run()
