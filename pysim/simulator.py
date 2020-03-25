import os
import bisect
import pandas as pd
from copy import deepcopy

from pysim.event import Event
from pysim.environment import Environment
from pysim.logger import logger
from pysim.experiment import ex


class Simulator(object):
    @ex.capture
    def __init__(self, sim_time_limit=10, experiment_dir=""):
        self.__sim_time_limit = sim_time_limit
        self.results_dir = 'results/' + experiment_dir

        self.__sim_time = 0
        self.__events = []
        self.__registered_modules = []
        self.__environment = Environment()

    def register_module(self, m, quantity=1):
        if m.get_name() not in self.__registered_modules:
            self.__registered_modules.append(m.get_name())

            if quantity == 1:
                self.__environment.add_item(m)
            else:
                for i in range(quantity):
                    module_copy = deepcopy(m)
                    module_copy.set_name("{}-{}".format(m.get_name(), i))
                    self.__environment.add_item(module_copy)
                del m
        else:
            logger.error("Duplicated module with same name {}".format(m.get_name()))
            exit(-1)

    def notify(self, e: Event):
        target = self.__environment.get(e.get_message().get_dest())

        if not target:
            logger.error("No module named {}".format(e.get_message().get_dest()))
            exit(-1)

        return target.notify(e)

    def run(self):
        for module in self.__environment.get_items().values():
            self.__events += module.load()

        while self.__events:
            self.forward()

        self.finish()

    def forward(self):
        if self.__events[0].get_time() > self.__sim_time_limit:
            self.__events.clear()
            return

        next_event = self.__events.pop(0)

        self.__sim_time = next_event.get_time()
        new_events = self.notify(next_event)

        del next_event

        while new_events:
            bisect.insort_left(self.__events, new_events.pop(0))

    def finish(self):
        for m in self.__environment.get_items().values():
            m.collect_signals()
            for signal in m.get_signals().values():
                self.dump_signal(m.get_name(), signal)

    def dump_signal(self, module_name, signal):
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

        df = pd.DataFrame({signal.get_name(): list(signal.get_records().values())})
        df.to_csv("{}/{}-{}.csv".format(self.results_dir, module_name, signal.get_name()))

    def __del__(self):
        self.__registered_modules.clear()
        self.__events.clear()
        del self.__environment
