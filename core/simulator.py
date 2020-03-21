import bisect
from core.baseModule import BaseModule
from core.event import Event
from datetime import datetime


class Simulator(object):
    def __init__(self):
        print("New simulation is started at {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")))
        self.sim_time = 0

        self.modules = {}
        self.events = []

    def is_valid(self, m: BaseModule):
        return m.name not in self.modules.keys()

    def add_module(self, *args):
        for m in args:
            if isinstance(m, BaseModule) and self.is_valid(m):
                self.modules.update({m.name: m})
            else:
                raise Exception("Duplicated module with same name {}".format(m.name))

    def notify_all(self, e: Event):
        new_events = []
        targets = [self.modules.get(e.msg.dest)] if not e.msg.broadcast else [m for name, m in self.modules.items() if name != e.msg.src]

        if not targets:
            raise Exception("No module named {}".format(e.msg.dest))

        for module in targets:
            new_events += module.notify(e)

        return new_events

    def run(self):
        for module in self.modules.values():
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
