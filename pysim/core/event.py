class Event(object):
    def __init__(self, msg, time):
        self.__msg = msg
        self.__time = time

    def get_message(self):
        return self.__msg

    def get_time(self):
        return self.__time

    def __lt__(self, other):
        return self.__time < other.__time

    def __del__(self):
        del self.__msg

    def __str__(self):
        return "msg:{} time:{}".format(self.__msg, self.__time)
