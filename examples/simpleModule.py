from core.baseModule import BaseModule
from core.message import Message
from core.simulator import sim


class SimpleModule(BaseModule):
    def initialize(self):
        if self.name == "s1":
            msg = Message("echo")
            self.send(msg, "s2", delay=1)
            print("[{}][{}] Send message {} to {} with delay 1".format(sim.sim_time, self.name, msg.text, msg.dest))

    def handle_message(self, msg):
        """ On message reception """
        if msg.dest == self.name:
            print("[{}][{}] Received new message {}".format(sim.sim_time, self.name, msg.text))

            if self.name == "s2":
                m = Message("reply")
                self.send(m, "s1", delay=1)
