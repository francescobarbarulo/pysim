from pysim.core.modules.baseModule import BaseModule
from pysim.core.message import Message

from pysim.examples.airport.passenger import Passenger


class Gate(BaseModule):
    def __init__(self, name):
        super(Gate, self).__init__(name)

        self.checkin_luggage_time = 10  # time to check-in a luggage
        self.hostess = None
        self.queue = []

    def handle_message(self, msg):
        if msg.is_self_message():
            # check-in done
            self.log("Passenger {} served".format(self.hostess.name))

            if self.queue:
                # if there is other passengers in the queue the hostess serves the first
                passenger = self.queue.pop(0)
                self.hostess = passenger

                delay = self.checkin_luggage_time * passenger.luggages
                self.log("Passenger {} with {} luggages served in {} seconds".format(passenger.name, passenger.luggages, delay))
                self.schedule_at(Message(), delay)
            else:
                # no passengers in the queue
                self.hostess = None

        else:
            if isinstance(msg, Passenger):
                # New passenger arrived in the queue
                passenger = msg

                if self.hostess is None:
                    # if the hostess for the check-in is free the passenger is served
                    self.hostess = passenger
                    delay = self.checkin_luggage_time * passenger.luggages
                    self.log("Passenger {} with {} luggages served in {} seconds".format(passenger.name, passenger.luggages, delay))
                    self.schedule_at(Message(), delay)
                else:
                    # the passenger stays in the queue
                    self.queue.append(passenger)

            else:
                # PG is asking for the queue length
                self.send(Message(len(self.queue) + bool(self.hostess)), msg.get_source())
