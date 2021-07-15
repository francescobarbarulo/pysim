import statistics
from typing import Dict, List

from pysim.core.experiment import ex
from pysim.core.event import Event
from pysim.core.message import Message
from pysim.core.signal import Signal, SignalType
from pysim.core.logger import logger


class BaseModule:
    @ex.capture
    def __init__(self, name: str, debug: bool = True) -> None:
        self._name: str = name
        self._sim_time: float = 0

        self._events: List[Event] = []
        self._signals: Dict[Signal, str] = {}

        self.debug: bool = debug


    def set_name(self, name: str) -> None:
        self._name = name


    def get_name(self) -> str:
        return self._name


    def sim_time(self) -> str:
        return self._sim_time


    def load(self) -> List[Event]:
        self.initialize()

        events: List[Event] = []

        while self._events:
            events.append(self._events.pop(0))

        return events


    def send(self, *, msg: Message, dest: str, delay: float = 0) -> None:
        msg.set_source(self._name)
        msg.set_dest(dest)

        e: Event = Event(msg, dest, self._sim_time + delay)
        self._events.append(e)


    def schedule_at(self, *, msg: Message, delay: float = 0) -> None:
        self.send(msg=msg, dest=self._name, delay=delay)


    def notify(self, e: Event) -> List[Event]:
        self._sim_time = e.get_time()

        self.handle_message(e.get_message())

        new_events: List[Event] = []
        while self._events:
            new_events.append(self._events.pop(0))

        return new_events


    def register_signal(self, *, name: str, signal_type: SignalType) -> None:
        if name not in self._signals.keys():
            self._signals.update({name: Signal(name, signal_type)})
        else:
            logger.error("Duplicated signals with name %s for module %s", name, self._name)
            exit(-1)


    def get_signals(self) -> Dict[Signal, str]:
        return self._signals


    def emit(self, *, signal_name: str, value: float) -> None:
        signal: Signal = self._signals.get(signal_name)

        if signal is None:
            logger.error("Signal %s not registered", signal_name)
            exit(-1)

        signal.emit(self._sim_time, value)


    def collect_signals(self) -> None:
        for signal in self._signals.values():
            if signal.get_records():
                if signal.get_stat_type() == SignalType.MEAN:
                    print("[{}] {}: {}".format(self._name, signal.get_name(), statistics.mean(signal.get_records().values())))


    def log(self, *, text: str) -> None:
        if self.debug:
            logger.info("[%.3f][%s] %s", self._sim_time, self._name, text)


    def __del__(self) -> None:
        self.finish()

        self._events.clear()
        self._signals.clear()


    def initialize(self) -> None:
        """
        The module that starts the interaction must implement this method
        with at least one send() or schedule_at() call
        """
        pass


    def handle_message(self, msg: Message) -> None:
        """
        Called whenever the module receives a message.
        Here the message can be consumed
        """
        pass


    def finish(self) -> None:
        """ 
        Here delete data structures used by your module
        """
        pass
