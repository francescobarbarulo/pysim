from pysim.core.experiment import ex
from pysim.core.modules.baseModule import BaseModule
from pysim.core.message import Message
from pysim.core.prng import PRNG

from pysim.examples.airport.passenger import Passenger


class PassengerGenerator(BaseModule):
    @ex.capture
    def __init__(self, name, airport_gates):
        super(PassengerGenerator, self).__init__(name)
        self.num_gates = airport_gates
        self.counter = 0

        self.msg_counter = 0
        self.min_queue = -1
        self.best_gate = None

    def initialize(self):
        # Start the generation
        self.schedule_at(Message())

    def handle_message(self, msg):
        if msg.is_self_message():
            # Generate a new passenger
            self.reset()

            self.log("New passenger generated")
            for g in range(self.num_gates):
                # Knowing which gate has less passengers in the queue
                self.send(Message(), "gate-{}".format(g))

        else:
            # Gates returned their queue length
            if self.msg_counter < self.num_gates:
                # still waiting for all lengths
                self.log("{}: {}".format(msg.get_source(), msg.get_text()))

                # update the best gate
                if self.min_queue < 0:
                    self.min_queue = int(msg.get_text())
                    self.best_gate = msg.get_source()
                else:
                    if int(msg.get_text()) < self.min_queue:
                        self.min_queue = int(msg.get_text())
                        self.best_gate = msg.get_source()

                self.msg_counter += 1

            if self.msg_counter >= self.num_gates:
                # All the lengths received: the passenger can be enqueued in the best gate
                # The number of luggages are generated uniformly random
                passenger = Passenger(self.counter, PRNG.intuniform(0, 3))
                self.log("Passenger {} with {} luggages in {}".format(passenger.name, passenger.luggages, self.best_gate))
                self.send(passenger, self.best_gate)

                self.counter += 1

                self.schedule_at(Message(), PRNG.exponential(1.5))

    def reset(self):
        self.min_queue = -1
        self.best_gate = None
        self.msg_counter = 0
