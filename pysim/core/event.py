class Event(object):
    def __init__(self, msg, target, time):
        self._msg = msg
        self._time = time
        self._target = target

    def get_message(self):
        return self._msg

    def get_target(self):
        return self._target

    def get_time(self):
        return self._time

    def __lt__(self, other):
        return self._time < other.get_time()

    def __del__(self):
        del self._msg

    def __str__(self):
        return "elem:{} time:{}".format(self._msg, self._time)
