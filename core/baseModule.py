from core.event import Event
from core.message import Message


class BaseModule(object):
    def __init__(self, name: str):
        self.name = name
        self.sim_time = 0
        self.events = []

        self.initialize()

    def load(self):
        events = []

        while self.events:
            events.append(self.events.pop(0))

        return events

    def send(self, msg: Message, dest: str, delay=0):
        msg.src = self.name
        msg.dest = dest

        e = Event(msg, self.sim_time + delay)
        self.events.append(e)

    def schedule_at(self, msg: Message, delay=0):
        self.send(msg, self.name, delay)

    def broadcast(self, msg: Message, delay=0):
        msg.broadcast = True
        self.send(msg, None, delay)

    def notify(self, e: Event):
        self.sim_time = e.time
        self.handle_message(e.msg)

        new_events = []
        while self.events:
            new_events.append(self.events.pop(0))

        return new_events

    def __del__(self):
        self.finish()

        for e in self.events:
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
