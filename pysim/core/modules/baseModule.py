import statistics

from pysim.core.experiment import ex
from pysim.core.event import Event
from pysim.core.message import Message
from pysim.core.movement import Movement
from pysim.core.signal import Signal
from pysim.core.logger import logger


class BaseModule(object):
    @ex.capture
    def __init__(self, name, debug=True):
        self._name = name
        self._sim_time = 0

        self._events = []
        self._signals = {}

        self.debug = debug

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def sim_time(self):
        return self._sim_time

    def load(self):
        self.move()
        self.initialize()

        events = []

        while self._events:
            events.append(self._events.pop(0))

        return events

    def send(self, msg: Message, dest, delay=0):
        msg.set_source(self._name)
        msg.set_dest(dest)

        e = Event(msg, dest, self._sim_time + delay)
        self._events.append(e)

    def schedule_at(self, msg: Message, delay=0):
        if isinstance(msg, Movement):
            e = Event(msg, self._name, self._sim_time + delay)
            self._events.append(e)
        else:
            self.send(msg, self._name, delay)

    def notify(self, e: Event):
        self._sim_time = e.get_time()

        if isinstance(e.get_message(), Movement):
            self.move()
        else:
            self.handle_message(e.get_message())

        new_events = []
        while self._events:
            new_events.append(self._events.pop(0))

        return new_events

    def register_signal(self, name, signal_type):
        if name not in self._signals.keys():
            self._signals.update({name: Signal(name, signal_type)})
        else:
            logger.error("Duplicated signals with name {} for module {}".format(name, self._name))
            exit(-1)

    def get_signals(self):
        return self._signals

    def emit(self, signal_name, value):
        signal = self._signals.get(signal_name)

        if signal is None:
            logger.error("Signal {} not registered".format(signal_name))
            exit(-1)

        signal.emit(self._sim_time, value)

    def collect_signals(self):
        for signal in self._signals.values():
            if signal.get_records():
                if signal.get_stat_type() == "mean":
                    print("[{}] {}: {}".format(self._name, signal.get_name(), statistics.mean(signal.get_records().values())))

    def log(self, text):
        if self.debug:
            logger.info("[{}][{}] {}".format(self._sim_time, self._name, text))

    def __del__(self):
        self.finish()

        self._events.clear()
        self._signals.clear()

    def move(self):
        pass

    def initialize(self):
        """
        The module that starts the interaction must implement this method
        with at least one send() or schedule_at() call
        """
        pass

    def handle_message(self, msg):
        """
        It is called whenever the module receives a message.
        Here you can consume the message
        """
        pass

    def finish(self):
        """ You can use it for deleting data structures used by your module """
        pass
