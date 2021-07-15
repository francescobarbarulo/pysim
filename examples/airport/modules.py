from typing import cast
from pysim.core.message import Message
from pysim.core.experiment import ex
from pysim.core import prng
from pysim.core.signal import SignalType
from pysim.modules.baseModule import BaseModule


class GateInfo(Message):
  def __init__(self, passengers) -> None:
      super(GateInfo, self).__init__()

      self.passengers = passengers


class Passenger(Message):
    def __init__(self, name, luggages):
        super(Passenger, self).__init__()
        
        self.name = name
        self.luggages = luggages


class Gate(BaseModule):
    def __init__(self, name):
        super(Gate, self).__init__(name)

        self.checkin_luggage_time = 10  # time to check-in a luggage
        self.hostess = None
        self.queue = []

    def initialize(self) -> None:
        self.register_signal(name="queue_length", signal_type=SignalType.MEAN)

    def handle_message(self, msg):
        if msg.is_self_message():
            # check-in done
            self.log(text="Passenger {} served".format(self.hostess.name))

            if self.queue:
                # if there is other passengers in the queue the hostess serves the first
                passenger = self.queue.pop(0)
                self.hostess = passenger

                delay = self.checkin_luggage_time * passenger.luggages
                self.log(text="Serving passenger {}".format(passenger.name))
                self.schedule_at(msg=Message(), delay=delay)
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
                    self.log(text="Serving passenger {}".format(passenger.name))
                    self.schedule_at(msg=Message(), delay=delay)
                else:
                    # the passenger stays in the queue
                    self.queue.append(passenger)

                self.emit(signal_name="queue_length", value=len(self.queue))

            else:
                # PG is asking for the queue length
                hostess = [self.hostess] if self.hostess else []
                self.send(msg=GateInfo(passengers=hostess + self.queue), dest=msg.get_source())


class PassengerGenerator(BaseModule):
    @ex.capture
    def __init__(self, name, airport_gates):
        super(PassengerGenerator, self).__init__(name)
        self.id = 0

        self.gates_status = {'gate-{}'.format(i): -1 for i in range(airport_gates)}

    def initialize(self):
        # Start the generation
        self.schedule_at(msg=Message())

    def handle_message(self, msg):
        if msg.is_self_message():
            # Reset gates status
            self.gates_status.update({k: -1 for k in self.gates_status.keys()})

            # Generate a new passenger
            self.log(text="New passenger generated")
            for gate in self.gates_status.keys():
                # Knowing which gate has less passengers in the queue
                self.send(msg=Message(), dest=gate)

        else:
            # A gate returned its queue
            gate_info = cast(GateInfo, msg)
            if -1 in list(self.gates_status.values()):
                # still waiting for all lengths
                self.log(text="{}: {}".format(msg.get_source(), [passenger.name for passenger in gate_info.passengers]))

                # update the gates status
                self.gates_status.update({msg.get_source(): len(gate_info.passengers)})

            if -1 not in list(self.gates_status.values()):
                # All the lengths received: the passenger can be enqueued in the best gate
                best_gate = min(self.gates_status, key=self.gates_status.get)

                # The number of luggages are generated uniformly random
                passenger = Passenger(self.id, prng.intuniform(0, 3))

                self.log(text="Passenger {} with {} luggages in {}".format(passenger.name, passenger.luggages, best_gate))
                self.send(msg=passenger, dest=best_gate)

                self.id += 1
                self.schedule_at(msg=Message(), delay=prng.exponential(8))
