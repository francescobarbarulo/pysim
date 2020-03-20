from baseModule import BaseModule
from core.message import Message
from core import sim


class SimpleModule(BaseModule):
    def initialize(self):
        msg = Message("echo", self.name)
        print("[{}][{}] Send message {} to {} with delay 1".format(sim.sim.sim_time, self.name, msg.text, msg.dest))
        self.send(msg, delay=1)

    def handle_message(self, msg):
        """ On message reception """
        if msg.dest == self.name:
            print("[{}][{}] Received new message {} created on {}".format(sim.sim.sim_time, self.name, msg.text, msg.created_on))
            #msg.dest = "s1" if self.name == "s2" else "s2"
            #print("[{}][{}] Send message {} to {} with delay 1".format(sim.sim.sim_time, self.name, msg.text, msg.dest))
            #self.send(msg, delay=1)
