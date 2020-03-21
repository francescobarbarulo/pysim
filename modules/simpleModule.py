"""
    Modules are derived by the main class BaseModule
    Custom modules have only to implement methods:
    - initialize(): where a first message must be send in order to start the simulation
    - handle_message(msg): called whenever a module receive a message

    Do not implement other methods than these
"""

from core.baseModule import BaseModule
from core.message import Message


class SimpleModule(BaseModule):
    def initialize(self):
        if self.name == "s1":
            msg = Message("echo")
            self.send(msg, "s2", delay=1)
            print("[{}][{}] Send message {} to {} with delay 1".format(self.sim_time, self.name, msg.text, msg.dest))

    def handle_message(self, msg):
        """ On message reception """
        if msg.dest == self.name:
            print("[{}][{}] Received new message {}".format(self.sim_time, self.name, msg.text))

            if self.name == "s2":
                m = Message("reply")
                self.send(m, "s1", delay=1)
                print("[{}][{}] Send message {} to {} with delay 1".format(self.sim_time, self.name, m.text, m.dest))