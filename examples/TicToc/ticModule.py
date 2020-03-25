from pysim.modules.baseModule import BaseModule
from pysim.message import Message
import time


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

        m = Message()
        dest = "toc"
        self.send(m, dest, delay=1)
        self.log("Send message {} to {}".format(m.get_text(), dest))

