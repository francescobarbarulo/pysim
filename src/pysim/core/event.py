from pysim.core.message import Message


class Event:
    def __init__(self, msg: Message, target: str, time: float) -> None:
        self._msg: Message = msg
        self._time: float = time
        self._target: str = target


    def get_message(self) -> Message:
        return self._msg


    def get_target(self) -> str:
        return self._target


    def get_time(self) -> float:
        return self._time


    def __lt__(self, other) -> bool:
        return self._time < other.get_time()


    def __del__(self) -> None:
        del self._msg


    def __str__(self) -> str:
        return "elem:{} time:{}".format(self._msg, self._time)
