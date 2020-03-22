from core.modules.baseModule import BaseModule
from core.message import Message
import time


class TicModule(BaseModule):
    def initialize(self):
        msg = Message("beep")
        self.schedule_at(msg)
        print("[{}][{}] Send self message {}".format(self.sim_time, self.name, msg.text))

    def handle_message(self, msg):
        if msg.is_self_message():
            print("[{}][{}] Received self message".format(self.sim_time, self.name))
        else:
            print("[{}][{}] Received new message {} from {}".format(self.sim_time, self.name, msg.text, msg.src))

        m = Message()
        dest = "toc"
        self.send(m, dest, delay=1)
        print("[{}][{}] Send message {} to {}".format(self.sim_time, self.name, m.text, dest))

        time.sleep(1)

