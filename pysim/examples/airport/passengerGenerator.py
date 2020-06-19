from pysim.core.experiment import ex
from pysim.core.modules.baseModule import BaseModule
from pysim.core.message import Message
import pysim.core.PRNG as PRNG

from pysim.examples.airport.passenger import Passenger


class PassengerGenerator(BaseModule):
    @ex.capture
    def __init__(self, name, airport_gates):
        super(PassengerGenerator, self).__init__(name)
        self.id = 0

        self.gates_status = {'gate-{}'.format(i): -1 for i in range(airport_gates)}

    def initialize(self):
        # Start the generation
        self.schedule_at(Message())

    def handle_message(self, msg):
        if msg.is_self_message():
            # Reset gates status
            self.gates_status.update({k: -1 for k in self.gates_status.keys()})

            # Generate a new passenger
            self.log("New passenger generated")
            for g in self.gates_status.keys():
                # Knowing which gate has less passengers in the queue
                self.send(Message(), g)

        else:
            # Gates returned their queue length
            if -1 in list(self.gates_status.values()):
                # still waiting for all lengths
                self.log("{}: {}".format(msg.get_source(), msg.get_text()))

                # update the gates status
                self.gates_status.update({msg.get_source(): int(msg.get_text())})

            if -1 not in list(self.gates_status.values()):
                # All the lengths received: the passenger can be enqueued in the best gate
                best_gate = min(self.gates_status, key=self.gates_status.get)
                # The number of luggages are generated uniformly random
                passenger = Passenger(self.id, PRNG.intuniform(0, 3))
                self.log("Passenger {} with {} luggages in {}".format(passenger.name, passenger.luggages, best_gate))
                self.send(passenger, best_gate)

                self.id += 1

                self.schedule_at(Message(), PRNG.exponential(1.5))
