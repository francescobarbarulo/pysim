from core.modules.baseModule import BaseModule
from core.message import Message


class ReplyModule(BaseModule):
    def handle_message(self, msg):
        print("[{}][{}] Received new message {} from {}".format(self.sim_time, self.name, msg.text, msg.src))

        m = Message(msg.text)
        self.send(m, msg.src, delay=1)
        print("[{}][{}] Send message {} to {}".format(self.sim_time, self.name, m.text, msg.src))
