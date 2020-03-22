import bisect
from datetime import datetime
import statistics
import random
import sys, os
from configparser import ConfigParser

from core.modules.baseModule import BaseModule
from core.event import Event


class Simulator(object):
    def __init__(self):
        self.__config = "pysim.ini"
        self.__sim_time = 0
        self.__sim_time_limit = 0
        self.__repeat = 0

        self.modules = {}
        self.events = []

        self.configure()

        print("New session is started at {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")))
        print("Number of repetitions set to {}".format(self.__repeat))

    def configure(self):
        config = ConfigParser()
        config.read(self.__config)

        self.__sim_time_limit = int(config["DEFAULT"]["sim_time_limit"])
        self.__repeat = int(config["DEFAULT"]["repeat"])

    def is_valid(self, m: BaseModule):
        return m.get_name() not in self.modules.keys()

    def register_module(self, *args):
        for m in args:
            if self.is_valid(m):
                self.modules.update({m.get_name(): m})
            else:
                raise Exception("Duplicated module with same name {}".format(m.get_name()))

    def notify(self, e: Event):
        target = self.modules.get(e.get_message().get_dest())

        if not target:
            raise Exception("No module named {}".format(e.get_message().get_dest()))

        return target.notify(e)

    def run(self):
        for repeat in range(self.__repeat):
            print("*** Simluation #{} ***".format(repeat))
            random.seed(repeat)
            self.reset()

            for module in self.modules.values():
                self.events += module.load()

            while self.events:
                self.forward()

    def forward(self):
        if self.events[0].get_time() > self.__sim_time_limit:
            self.finish()
            return

        next_event = self.events.pop(0)

        self.__sim_time = next_event.get_time()
        new_events = self.notify(next_event)

        del next_event

        while new_events:
            bisect.insort_left(self.events, new_events.pop(0))

    def finish(self):
        self.events.clear()

        self.collect_signals()

    def collect_signals(self):
        for m in self.modules.values():
            for signal in m.get_signals().values():
                if signal.get_stat_type() == "mean":
                    print("{}: {}".format(signal.get_name(), statistics.mean(signal.get_records())))

    def reset(self):
        self.__sim_time = 0

        for m in self.modules.values():
            m.reset()

    def __del__(self):
        for m in self.modules.values():
            del m

        for e in self.events:
            del e

        print("Session finished at {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")))
