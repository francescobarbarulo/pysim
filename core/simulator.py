import bisect
import random
from copy import deepcopy
from datetime import datetime
from configparser import ConfigParser

from core.event import Event
from core.environment import Environment


class Simulator(object):
    def __init__(self):
        self.__config_file = "pysim.ini"
        self.__config = ConfigParser()

        self.__sim_time = 0
        self.__sim_time_limit = 0
        self.__repeat = 0
        self.__warm_up_period = 0

        self.modules = {}
        self.events = []
        self.environment = None

        print("New session is started at {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")))
        print("Number of repetitions set to {}".format(self.__repeat))

    def register_module(self, *args):
        for m in args:
            if m.get_name() not in self.modules.keys():
                self.modules.update({m.get_name(): m})
            else:
                raise Exception("Duplicated module with same name {}".format(m.get_name()))

    def configure(self):
        self.__config.read(self.__config_file)

        if "sim_time_limit" in self.__config["DEFAULT"]:
            self.__sim_time_limit = int(self.__config["DEFAULT"]["sim_time_limit"])

        if "repeat" in self.__config["DEFAULT"]:
            self.__repeat = int(self.__config["DEFAULT"]["repeat"])

        if "warm_up_period" in self.__config["DEFAULT"]:
            self.__warm_up_period = int(self.__config["DEFAULT"]["warm_up_period"])

        self.set_environment()

    def set_environment(self):
        self.environment = Environment()

        names = [n for n in self.modules.keys()]

        for n in names:
            m = self.modules.pop(n)
            m._warm_up_period = self.__warm_up_period

            if "Environment" in self.__config and n in self.__config['Environment']:
                qty = int(self.__config['Environment'][n])
                for i in range(qty):
                    item = deepcopy(m)
                    item.set_name("{}-{}".format(n, i))
                    self.environment.add_item(item)
            else:
                self.environment.add_item(m)

    def notify(self, e: Event):
        target = self.environment.get(e.get_message().get_dest())

        if not target:
            raise Exception("No module named {}".format(e.get_message().get_dest()))

        return target.notify(e)

    def run(self):
        self.configure()

        print(self.environment)

        for repeat in range(self.__repeat):
            print("*** Simulation #{} ***".format(repeat))
            random.seed(repeat)
            self.reset()

            for module in self.environment.get_items().values():
                self.events += module.load()

            while self.events:
                self.forward()

            self.finish()

    def forward(self):
        if self.events[0].get_time() > self.__sim_time_limit:
            self.events.clear()
            return

        next_event = self.events.pop(0)

        self.__sim_time = next_event.get_time()
        new_events = self.notify(next_event)

        del next_event

        while new_events:
            bisect.insort_left(self.events, new_events.pop(0))

    def finish(self):
        for m in self.environment.get_items().values():
            m.collect_signals()

    def reset(self):
        self.__sim_time = 0

        for m in self.environment.get_items().values():
            m.reset()

    def __del__(self):
        self.events.clear()

        del self.__config
        del self.environment

        print("Session finished at {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")))
