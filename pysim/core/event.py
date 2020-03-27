class Event(object):
    def __init__(self, elem, target, time):
        self.__elem = elem
        self.__time = time
        self.__target = target

    def get_elem(self):
        return self.__elem

    def get_target(self):
        return self.__target

    def get_time(self):
        return self.__time

    def __lt__(self, other):
        return self.__time < other.__time

    def __del__(self):
        del self.__elem

    def __str__(self):
        return "elem:{} time:{}".format(self.__elem, self.__time)
