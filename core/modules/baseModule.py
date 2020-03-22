from core.event import Event
from core.signal import Signal


class BaseModule(object):
    def __init__(self, name):
        self.__name = name
        self.__sim_time = 0
        self.__events = []
        self.__signals = {}

    def get_name(self):
        return self.__name

    def sim_time(self):
        return self.__sim_time

    def load(self):
        self.initialize()

        events = []

        while self.__events:
            events.append(self.__events.pop(0))

        return events

    def send(self, msg, dest, delay=0):
        msg.set_source(self.__name)
        msg.set_dest(dest)

        e = Event(msg, self.__sim_time + delay)
        self.__events.append(e)

    def schedule_at(self, msg, delay=0):
        self.send(msg, self.__name, delay)

    def notify(self, e):
        self.__sim_time = e.get_time()
        self.handle_message(e.get_message())

        new_events = []
        while self.__events:
            new_events.append(self.__events.pop(0))

        return new_events

    def register_signal(self, name, signal_type):
        if name not in self.__signals.keys():
            self.__signals.update({name: Signal(name, signal_type)})
        else:
            raise Exception("Duplicated signals with name {}".format(name))

    def get_signals(self):
        return self.__signals

    def emit(self, signal_name, value):
        signal = self.__signals.get(signal_name)

        if signal is None:
            raise Exception("Signal {} not registered".format(signal_name))

        signal.emit(value)

    def reset(self):
        self.__sim_time = 0
        self.__events.clear()
        for s in self.__signals.values():
            s.reset()

    def __del__(self):
        self.finish()

        for e in self.__events:
            del e

    def initialize(self):
        """
        The module that starts the interaction must implement this method
        with at least one send() call
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
