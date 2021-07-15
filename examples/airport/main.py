from pysim.core.simulator import Simulator
from pysim.core.experiment import ex

from modules import PassengerGenerator, Gate


@ex.config
def config():
    airport_gates = 2


@ex.automain
def main(airport_gates):
    sim = Simulator()

    sim.register_module(create_module=PassengerGenerator, name="PG")
    sim.register_module(create_module=Gate, name="gate", quantity=airport_gates)

    sim.run()
