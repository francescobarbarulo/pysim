from pysim.core.simulator import Simulator
from pysim.core.experiment import ex

from pysim.examples.airport.passengerGenerator import PassengerGenerator
from pysim.examples.airport.gate import Gate


@ex.config
def config():
    airport_gates = 2


@ex.automain
def main(airport_gates):
    sim = Simulator()

    sim.register_module(PassengerGenerator, "PG")
    sim.register_module(Gate, "gate", airport_gates)

    sim.run()
