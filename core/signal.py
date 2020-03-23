class Signal(object):
    def __init__(self, name, stat_type):
        self.__name = name
        self.__stat_type = stat_type
        self.__records = {}

    def emit(self, time, value):
        self.__records.update({time: value})

    def get_name(self):
        return self.__name

    def get_stat_type(self):
        return self.__stat_type

    def get_records(self):
        return self.__records.values()

    def reset(self):
        self.__records.clear()
