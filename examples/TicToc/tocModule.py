from pysim.modules.baseModule import BaseModule
from pysim.message import Message
import time


class TocModule(BaseModule):
    def handle_message(self, msg):
        self.log("Received new message {} from {}".format(msg.get_text(), msg.get_source()))

        m = Message()
        self.send(m, msg.get_source(), delay=1)
        self.log("Send message {} to {}".format(m.get_text(), msg.get_source()))

