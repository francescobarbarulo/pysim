from simpleModule import SimpleModule
from core.message import Message
from core import sim
import time


class TicTocModule(SimpleModule):
    def initialize(self):
        dest = "s1" if self.name == "s2" else "s2"
        msg = Message("echo", dest)
        print("[{}][{}] Send message {} to {} with delay 1".format(sim.sim.sim_time, self.name, msg.text, msg.dest))
        self.send(msg, delay=1)

    def handle_message(self, msg):
        """ On message reception """
        if msg.dest == self.name:
            print("[{}][{}] Received new message {}".format(sim.sim.sim_time, self.name, msg.text))
            msg.dest = "s1" if self.name == "s2" else "s2"
            print("[{}][{}] Send message {} to {} with delay 1".format(sim.sim.sim_time, self.name, msg.text, msg.dest))
            self.send(msg, delay=1)
        else:
            print("[{}][{}] not for me".format(sim.sim.sim_time, self.name))

        time.sleep(1)
