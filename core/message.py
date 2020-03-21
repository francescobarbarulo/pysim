from core.simulator import sim


class Message(object):
    def __init__(self, text):
        self.text = text
        self.src = None
        self.dest = None
        self.created_on = sim.sim_time

    def is_self_message(self):
        return self.src == self.dest
