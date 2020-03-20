from core.sim import *
from core.event import Event
from core import sim


class BaseModule(object):
    def __init__(self, name):
        self.name = name
        self.events = []

        self.initialize()

    def load(self):
        events = []
        for e in self.events:
            events.append(e)

        self.events.clear()
        return events

    def send(self, msg, **kwargs):
        delay = kwargs['delay'] if 'delay' in kwargs else 0

        e = Event(msg, sim.sim.sim_time + delay)
        self.events.append(e)

    def notify(self, e):
        print("notify")
        self.handle_message(e.msg)

        new_events = []
        for e in self.events:
            new_events.append(e)
        self.events.clear()

        return new_events

    # The next functions have to be implemented by your modules

    def initialize(self):
        pass

    def handle_message(self, msg):
        pass
