from pysim.modules.baseModule import BaseModule
from pysim.message import Message


class EchoModule(BaseModule):
    def initialize(self):
        msg = Message()
        self.send(msg, "reply", delay=1)
        print("[{}][{}] Send message {} to {}".format(self.sim_time(), self.get_name(), msg.get_text(), msg.get_dest()))

    def handle_message(self, msg):
        print("[{}][{}] Received new message {} from {}".format(self.sim_time(), self.get_name(), msg.get_text(), msg.get_source()))
