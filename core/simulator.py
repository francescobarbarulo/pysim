import bisect
from core.baseModule import BaseModule
from core.event import Event
from datetime import datetime


class Simulator(object):
    def __init__(self):
        print("New simulation is started at {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")))
        self.sim_time = 0

        self.modules = []
        self.events = []

    def is_valid(self, m: BaseModule):
        names = [m.name for m in self.modules]
        return m.name not in names

    def add_module(self, *args):
        for m in args:
            if isinstance(m, BaseModule) and self.is_valid(m):
                self.modules.append(m)
            else:
                raise Exception("module {0} has not been added because it already exists".format(m.name))

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

        del next_event

        while new_events:
            bisect.insort_left(self.events, new_events.pop(0))

    def __del__(self):
        for m in self.modules:
            del m

        for e in self.events:
            del e

        print("Simulation finished at {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")))
