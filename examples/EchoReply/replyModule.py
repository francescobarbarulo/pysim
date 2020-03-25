from pysim.modules.baseModule import BaseModule
from pysim.message import Message


class ReplyModule(BaseModule):
    def handle_message(self, msg):
        print("[{}][{}] Received new message {} from {}".format(self.sim_time(), self.get_name(), msg.get_text(), msg.get_source()))

        m = Message(msg.get_text())
        self.send(m, msg.get_source(), delay=1)
        print("[{}][{}] Send message {} to {}".format(self.sim_time(), self.get_name(), m.get_text(), msg.get_source()))
