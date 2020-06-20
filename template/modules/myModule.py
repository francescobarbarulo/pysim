from pysim.core.experiment import ex
from pysim.core.modules.baseModule import BaseModule


class MyModule(BaseModule):
    @ex.capture
    def __init__(self, name):
        super(MyModule, self).__init__(name)

    def initialize(self):
        pass

    def handle_message(self, msg):
        pass

    def finish(self):
        pass
