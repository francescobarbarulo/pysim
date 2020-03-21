class Event(object):
    def __init__(self, msg, time):
        self.msg = msg
        self.time = time

    def __lt__(self, other):
        self.time < other.time

    def __del__(self):
        del self.msg
