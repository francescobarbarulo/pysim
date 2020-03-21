"""
    Modules are derived by the main class BaseModule
    Custom modules have only to implement methods:
    - initialize(): where a first message must be send in order to start the simulation
    - handle_message(msg): called whenever a module receive a message

    Do not implement other methods than these
"""

from core.baseModule import BaseModule
from core.message import Message
import time


class TicTocModule(BaseModule):
    def initialize(self):
        if self.name == "s1":
            msg = Message("beep")
            self.send(msg, "s1", delay=0)
            print("[{}][{}] Send message {} to {}".format(self.sim_time, self.name, msg.text, msg.dest))

    def handle_message(self, msg):
        """ On message reception """
        if msg.dest == self.name:
            print("[{}][{}] Received new message {}".format(self.sim_time, self.name, msg.text))
            delay = 1
            if self.name == "s1":
                m = Message("tic")
                dest = "s2"

            else:
                m = Message("toc")
                dest = "s1"

            self.send(m, dest, delay=delay)
            print("[{}][{}] Send message {} to {} with delay {}".format(self.sim_time, self.name, m.text, dest, delay))

            time.sleep(1)

