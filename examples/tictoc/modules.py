from pysim.core.message import Message
from pysim.modules.baseModule import BaseModule


class TicModule(BaseModule):
    def initialize(self) -> None:
        msg: Message = Message("beep")
        self.schedule_at(msg=msg)
        self.log(text="Send self message {}".format(msg.get_text()))

    def handle_message(self, msg: Message) -> None:
        if msg.is_self_message():
            self.log(text="Received self message")
        else:
            self.log(text="Received new message {} from {}".format(msg.get_text(), msg.get_source()))

        message: Message = Message("hello")
        self.send(msg=message, dest="toc", delay=1)
        self.log(text="Send message {} to {}".format(message.get_text(), message.get_dest()))


class TocModule(BaseModule):
    def handle_message(self, msg: Message) -> None:
        self.log(text="Received new message {} from {}".format(msg.get_text(), msg.get_source()))

        self.send(msg=msg, dest=msg.get_source(), delay=1)
        self.log(text="Send message {} to {}".format(msg.get_text(), msg.get_dest()))