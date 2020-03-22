from core.modules.baseModule import BaseModule
from core.message import Message


class SampleModule(BaseModule):
    def __init__(self, name):
        # here data structures can be defined, for instance
        self.queue = []
        # the call to the base class constructor must be the last
        super(SampleModule, self).__init__(name)

    def initialize(self):
        # initialize your data structures, for instance
        self.queue.append(object)
        # if you want the module to start you need to schedule a message
        # so that it will trigger the handle_message function
        msg = Message()
        self.schedule_at(msg, delay=0)

    def handle_message(self, msg):
        # consume the message
        print("New message received\ntext: {}\nfrom: {}".format(msg.get_text(), msg.get_source()))

    def finish(self):
        # destroy all data structures, for instance
        for o in self.queue:
            del o
