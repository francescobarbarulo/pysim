from core.baseModule import BaseModule
from core.message import Message


class ReceiverModule(BaseModule):
    def handle_message(self, msg: Message):
        print("[{}][{}] Received message {} from {}".format(self.sim_time, self.name, msg.text, msg.src))
