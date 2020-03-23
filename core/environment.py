class Environment(object):
    def __init__(self):
        self.__items = {}

    def add_item(self, item):
        self.__items.update({item.get_name(): item})

    def get_items(self):
        return self.__items

    def get(self, name):
        return self.__items.get(name)

    def __str__(self):
        str = ""
        for n, m in self.__items.items():
            str += "{{{}: {}}} ".format(n, type(m))
        return str

    def __del__(self):
        self.__items.clear()
