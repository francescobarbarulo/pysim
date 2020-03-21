from core.baseModule import BaseModule
from core.message import Message


class BroadcastModule(BaseModule):
    def initialize(self):
        msg = Message()
        self.broadcast(msg, 5)

    def handle_message(self, msg: Message):
        print("[{}][{}] Received message {} from {}".format(self.sim_time, self.name, msg.text, msg.src))
