import os
import bisect
import pandas as pd
from copy import deepcopy

from pysim.core.event import Event
from pysim.core.environment import Environment
from pysim.core.logger import logger
from pysim.core.experiment import ex


class Simulator(object):
    @ex.capture
    def __init__(self, sim_time_limit=10, experiment_dir=""):
        self._sim_time_limit = sim_time_limit
        self._results_dir = 'results/' + experiment_dir

        self._sim_time = 0
        self._events = []
        self._registered_modules = []
        self._environment = Environment()

    def register_module(self, m, quantity=1):
        if m.get_name() not in self._registered_modules:
            self._registered_modules.append(m.get_name())

            if quantity == 1:
                self._environment.add_item(m)
            else:
                for i in range(quantity):
                    module_copy = deepcopy(m)
                    module_copy.set_name("{}-{}".format(m.get_name(), i))
                    self._environment.add_item(module_copy)
                del m
        else:
            logger.error("Duplicated module with same name {}".format(m.get_name()))
            exit(-1)

    def notify(self, e: Event):
        target = self._environment.get(e.get_target())

        if not target:
            logger.error("No module named {}".format(e.get_target()))
            exit(-1)

        return target.notify(e)

    def run(self):
        new_events = []

        for module in self._environment.get_items().values():
            new_events += module.load()

        while new_events:
            bisect.insort_left(self._events, new_events.pop(0))

        while self._events:
            self.forward()

        self.finish()

    def forward(self):
        if self._events[0].get_time() > self._sim_time_limit:
            self._events.clear()
            return

        next_event = self._events.pop(0)

        self._sim_time = next_event.get_time()
        new_events = self.notify(next_event)

        del next_event

        while new_events:
            bisect.insort_right(self._events, new_events.pop(0))

    def finish(self):
        for m in self._environment.get_items().values():
            m.collect_signals()
            for signal in m.get_signals().values():
                self.dump_signal(m.get_name(), signal)

    def dump_signal(self, module_name, signal):
        if not os.path.exists(self._results_dir):
            os.makedirs(self._results_dir)

        df = pd.DataFrame({signal.get_name(): list(signal.get_records().values())})
        df.to_csv("{}/{}-{}.csv".format(self._results_dir, module_name, signal.get_name()))

    def __del__(self):
        self._registered_modules.clear()
        self._events.clear()
        del self._environment
