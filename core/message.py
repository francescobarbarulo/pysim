class Message(object):
    def __init__(self, text="hello"):
        self.__text = text
        self.__src = None
        self.__dest = None

    def get_text(self):
        return self.__text

    def set_source(self, src):
        self.__src = src

    def get_source(self):
        return self.__src

    def set_dest(self, dest):
        self.__dest = dest

    def get_dest(self):
        return self.__dest

    def is_self_message(self):
        return self.__src == self.__dest
