from pysim.core.modules.baseModule import BaseModule


class TocModule(BaseModule):
    def handle_message(self, msg):
        self.log("Received new message {} from {}".format(msg.get_text(), msg.get_source()))

        self.send(msg, msg.get_source(), delay=1)
        self.log("Send message {} to {}".format(msg.get_text(), msg.get_dest()))

