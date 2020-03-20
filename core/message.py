from core import sim


class Message(object):
    def __init__(self, text, dest):
        self.text = text
        self.dest = dest
        self.created_on = sim.sim.sim_time
