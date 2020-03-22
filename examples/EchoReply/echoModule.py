from core.modules.baseModule import BaseModule
from core.message import Message


class EchoModule(BaseModule):
    def initialize(self):
        msg = Message()
        self.send(msg, "reply", delay=1)
        print("[{}][{}] Send message {} to {}".format(self.sim_time, self.name, msg.text, msg.dest))

    def handle_message(self, msg):
        print("[{}][{}] Received new message {} from {}".format(self.sim_time, self.name, msg.text, msg.src))
