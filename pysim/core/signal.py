from pysim.core.experiment import ex


class Signal(object):
    @ex.capture
    def __init__(self, name, stat_type, warm_up_period=0):
        self._name = name
        self._stat_type = stat_type
        self._records = {}

        self._warm_up_period = warm_up_period

    def emit(self, time, value):
        if time > self._warm_up_period:
            self._records.update({time: value})

    def get_name(self):
        return self._name

    def get_stat_type(self):
        return self._stat_type

    def get_records(self):
        return self._records

    def __del__(self):
        self._records.clear()
