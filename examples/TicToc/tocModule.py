from core.modules.baseModule import BaseModule
from core.message import Message
import time


class TocModule(BaseModule):
    def handle_message(self, msg):
        print("[{}][{}] Received new message {} from {}".format(self.sim_time(), self.get_name(), msg.get_text(), msg.get_source()))

        m = Message()
        self.send(m, msg.get_source(), delay=1)
        print("[{}][{}] Send message {} to {}".format(self.sim_time(), self.get_name(), m.get_text(), msg.get_source()))

        time.sleep(1)

