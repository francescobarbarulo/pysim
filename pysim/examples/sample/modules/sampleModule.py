from pysim.core.modules.baseModule import BaseModule
from pysim.core.message import Message


class SampleModule(BaseModule):
    def __init__(self, name):
        super(SampleModule, self).__init__(name)
        # here data structures can be defined, for instance
        self.queue = []

    def initialize(self):
        # if you want the module to start you need to schedule a message
        # so that it will trigger the handle_message function
        msg = Message("hello")
        self.schedule_at(msg, delay=0)

    def handle_message(self, msg):
        # consume the message
        self.log("Message '{}' received from {}".format(msg.get_text(), msg.get_source()))
        self.queue.append(msg)

    def finish(self):
        # destroy all used data structures
        self.queue.clear()
