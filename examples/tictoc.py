from core.baseModule import BaseModule
from core.message import Message
from core.simulator import sim
import time


class TicTocModule(BaseModule):
    def initialize(self):
        if self.name == "s1":
            msg = Message("beep")
            self.send(msg, "s1", delay=0)
            print("[{}][{}] Send message {} to {}".format(sim.sim_time, self.name, msg.text, msg.dest))

    def handle_message(self, msg):
        """ On message reception """
        if msg.dest == self.name:
            print("[{}][{}] Received new message {}".format(sim.sim_time, self.name, msg.text))
            if self.name == "s1":
                m = Message("tic")
                dest = "s2"

                self.send(m, dest, delay=3)
                self.send(m, dest, delay=2)
                print("[{}][{}] Send message {} to {}".format(sim.sim_time, self.name, m.text, dest))

            time.sleep(1)

