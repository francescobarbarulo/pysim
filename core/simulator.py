import bisect
from core.baseModule import BaseModule
from core.event import Event


class Simulator(object):
    def __init__(self):
        self.modules = []
        self.sim_time = 0
        self.events = []

    def add_module(self, m: BaseModule):
        self.modules.append(m)

    def notify_all(self, e: Event):
        new_events = []

        for module in self.modules:
            new_events += module.notify(e)

        return new_events

    def run(self):
        for module in self.modules:
            self.events += module.load()

        while self.events:
            self.forward()

    def forward(self):
        next_event = self.events.pop(0)

        self.sim_time = next_event.time
        new_events = self.notify_all(next_event)

        del next_event.msg
        del next_event

        while new_events:
            bisect.insort_left(self.events, new_events.pop(0))


sim = Simulator()
