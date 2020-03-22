"""
    Modules are derived by the main class BaseModule
    Custom examples have only to implement methods:
    - initialize(): where a first message must be send in order to start the simulation
    - handle_message(msg): called whenever a module receive a message

    Do not implement other methods than these
"""

from core.modules.baseModule import BaseModule
from core.message import Message


class EchoModule(BaseModule):
    def initialize(self):
        msg = Message()
        self.send(msg, "reply", delay=1)
        print("[{}][{}] Send message {} to {}".format(self.sim_time, self.name, msg.text, msg.dest))

    def handle_message(self, msg):
        print("[{}][{}] Received new message {} from {}".format(self.sim_time, self.name, msg.text, msg.src))
