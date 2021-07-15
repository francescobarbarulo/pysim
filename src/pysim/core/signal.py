from typing import Dict
from enum import Enum
from pysim.core.experiment import ex


class SignalType(str, Enum):
    MEAN = "mean"


class Signal:
    @ex.capture
    def __init__(self, name: str, stat_type: SignalType, warm_up_period: float = 0) -> None:
        self._name: str = name
        self._stat_type: str = stat_type
        self._records: Dict[float, float] = {}

        self._warm_up_period: float = warm_up_period


    def emit(self, time: float, value: float) -> None:
        if time > self._warm_up_period:
            self._records.update({time: value})


    def get_name(self) -> str:
        return self._name


    def get_stat_type(self) -> str:
        return self._stat_type


    def get_records(self) -> Dict[float, float]:
        return self._records


    def __del__(self) -> None:
        self._records.clear()
