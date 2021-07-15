import os
import bisect
from typing import Callable, List
import pandas as pd

from pysim.core.event import Event
from pysim.core.environment import Environment
from pysim.core.logger import logger
from pysim.core.experiment import ex
from pysim.core.signal import Signal
from pysim.modules.baseModule import BaseModule


class Simulator:
    @ex.capture
    def __init__(
        self,
        *,
        sim_time_limit: int = 10,
        experiment_dir: str = ""
    ) -> None:
        self._sim_time_limit: int = sim_time_limit
        self._results_dir: str = 'results/' + experiment_dir

        self._sim_time: int = 0
        self._events: List[Event] = []
        self._registered_modules: List[BaseModule] = []
        self._environment: Environment = Environment()


    def register_module(
        self,
        *,
        create_module: Callable[[str, bool], None],
        name: str,
        quantity: int = 1
    ) -> None:
        if name not in self._registered_modules:
            self._registered_modules.append(name)

            if quantity == 1:
                m: BaseModule = create_module(name)
                self._environment.add_item(m)
            else:
                for i in range(quantity):
                    m: BaseModule = create_module('{}-{}'.format(name, i))
                    self._environment.add_item(m)
        else:
            logger.error("Duplicated module with same name %s", name)
            exit(-1)


    def notify(self, e: Event) -> List[Event]:
        target: BaseModule = self._environment.get(e.get_target())

        if not target:
            logger.error("No module named %s", e.get_target())
            exit(-1)

        return target.notify(e)


    def run(self) -> None:
        new_events: List[Event] = []

        for module in self._environment.get_items().values():
            new_events += module.load()

        while new_events:
            bisect.insort_left(self._events, new_events.pop(0))

        while self._events:
            self.forward()

        self.finish()


    def forward(self) -> None:
        if self._events[0].get_time() > self._sim_time_limit:
            self._events.clear()
            return

        next_event: Event = self._events.pop(0)

        self._sim_time = next_event.get_time()
        new_events: List[Event] = self.notify(next_event)

        del next_event

        while new_events:
            bisect.insort_right(self._events, new_events.pop(0))


    def finish(self) -> None:
        for m in self._environment.get_items().values():
            m.collect_signals()
            for signal in m.get_signals().values():
                self.dump_signal(m.get_name(), signal)


    def dump_signal(self, module_name: str, signal: Signal) -> None:
        if not os.path.exists(self._results_dir):
            os.makedirs(self._results_dir)

        df = pd.DataFrame({signal.get_name(): list(signal.get_records().values())})
        df.to_csv("{}/{}-{}.csv".format(self._results_dir, module_name, signal.get_name()))


    def __del__(self) -> None:
        self._registered_modules.clear()
        self._events.clear()
        del self._environment
