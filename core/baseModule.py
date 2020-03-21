from core.simulator import sim
from core.event import Event
from core.message import Message


class BaseModule(object):
    def __init__(self, name: str):
        self.name = name
        self.events = []

        self.initialize()

    def load(self):
        events = []
        for e in self.events:
            events.append(e)

        self.events.clear()
        return events

    def send(self, msg: Message, dest: str, **kwargs):
        delay = kwargs['delay'] if 'delay' in kwargs else 0

        msg.src = self.name
        msg.dest = dest

        e = Event(msg, sim.sim_time + delay)
        self.events.append(e)

    def notify(self, e: Event):
        self.handle_message(e.msg)

        new_events = []
        for e in self.events:
            new_events.append(e)
        self.events.clear()

        return new_events

    # The next functions have to be implemented by your modules

    def initialize(self):
        pass

    def handle_message(self, msg: Message):
        pass
