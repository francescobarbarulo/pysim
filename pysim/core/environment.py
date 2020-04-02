class Environment(object):
    def __init__(self):
        self._items = {}

    def add_item(self, item):
        self._items.update({item.get_name(): item})

    def get_items(self):
        return self._items

    def get(self, name):
        return self._items.get(name)

    def __str__(self):
        str = ""
        for n, m in self._items.items():
            str += "{{{}: {}}} ".format(n, m)
        return str

    def __del__(self):
        self._items.clear()
