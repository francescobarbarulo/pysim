class Message(object):
    def __init__(self, text):
        self.text = text
        self.src = None
        self.dest = None

    def is_self_message(self):
        return self.src == self.dest
