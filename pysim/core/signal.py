from pysim.core.experiment import ex


class Signal(object):
    @ex.capture
    def __init__(self, name, stat_type, warm_up_period=0):
        self.__name = name
        self.__stat_type = stat_type
        self.__records = {}

        self.__warm_up_period = warm_up_period

    def emit(self, time, value):
        if time > self.__warm_up_period:
            self.__records.update({time: value})

    def get_name(self):
        return self.__name

    def get_stat_type(self):
        return self.__stat_type

    def get_records(self):
        return self.__records

    def reset(self):
        self.__records.clear()
