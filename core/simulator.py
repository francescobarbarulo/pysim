import bisect
from core.modules.baseModule import BaseModule
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

    def register(self, *args):
        for m in args:
            if isinstance(m, BaseModule) and self.is_valid(m):
                self.modules.update({m.name: m})
            else:
                raise Exception("Duplicated module with same name {}".format(m.name))

    def notify(self, e: Event):
        target = self.modules.get(e.msg.dest)

        if not target:
            raise Exception("No module named {}".format(e.msg.dest))

        return target.notify(e)

    def run(self):
        for module in self.modules.values():
            self.events += module.load()

        while self.events:
            self.forward()

    def forward(self):
        next_event = self.events.pop(0)

        self.sim_time = next_event.time
        new_events = self.notify(next_event)

        del next_event

        while new_events:
            bisect.insort_left(self.events, new_events.pop(0))

    def __del__(self):
        for m in self.modules.values():
            del m

        for e in self.events:
            del e

        print("Simulation finished at {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")))
