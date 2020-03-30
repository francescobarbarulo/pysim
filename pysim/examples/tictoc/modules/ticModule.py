from pysim.core.modules.baseModule import BaseModule
from pysim.core.message import Message


class TicModule(BaseModule):
    def initialize(self):
        msg = Message("beep")
        self.schedule_at(msg)
        self.log("Send self message {}".format(msg.get_text()))

    def handle_message(self, msg):
        if msg.is_self_message():
            self.log("Received self message")
        else:
            self.log("Received new message {} from {}".format(msg.get_text(), msg.get_source()))

        m = Message("hello")
        self.send(m, "toc", delay=1)
        self.log("Send message {} to {}".format(m.get_text(), m.get_dest()))

