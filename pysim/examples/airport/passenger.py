from pysim.core.message import Message


class Passenger(Message):
    def __init__(self, name, luggages):
        super(Passenger, self).__init__()
        
        self.name = name
        self.luggages = luggages
