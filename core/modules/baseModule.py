from core.event import Event
from core.message import Message


class BaseModule(object):
    def __init__(self, name: str):
        self.__name = name
        self.__sim_time = 0
        self.__events = []

        self.initialize()

    def get_name(self):
        return self.__name

    def sim_time(self):
        return self.__sim_time

    def load(self):
        events = []

        while self.__events:
            events.append(self.__events.pop(0))

        return events

    def send(self, msg: Message, dest: str, delay=0):
        msg.set_source(self.__name)
        msg.set_dest(dest)

        e = Event(msg, self.__sim_time + delay)
        self.__events.append(e)

    def schedule_at(self, msg: Message, delay=0):
        self.send(msg, self.__name, delay)

    def notify(self, e: Event):
        self.__sim_time = e.get_time()
        self.handle_message(e.get_message())

        new_events = []
        while self.__events:
            new_events.append(self.__events.pop(0))

        return new_events

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

    def handle_message(self, msg: Message):
        """
        It is called whenever the module receives a message.
        Here you can consume the message
        """
        pass

    def finish(self):
        """ You can use it for deleting data structures used by your module """
        pass
