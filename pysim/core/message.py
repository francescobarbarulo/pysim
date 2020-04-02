class Message(object):
    def __init__(self, text=None):
        self._text = text
        self._src = None
        self._dest = None

    def get_text(self):
        return self._text

    def set_source(self, src):
        self._src = src

    def get_source(self):
        return self._src

    def set_dest(self, dest):
        self._dest = dest

    def get_dest(self):
        return self._dest

    def is_self_message(self):
        return self._src == self._dest
