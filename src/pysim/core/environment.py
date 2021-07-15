from typing import Dict

from pysim.modules.baseModule import BaseModule


class Environment:
    def __init__(self) -> None:
        self._items: Dict[str, BaseModule] = {}


    def add_item(self, item: BaseModule) -> None:
        self._items.update({item.get_name(): item})


    def get_items(self) -> Dict[str, BaseModule]:
        return self._items


    def get(self, name: str) -> BaseModule:
        return self._items.get(name)


    def __str__(self) -> str:
        str = ""
        for n, m in self._items.items():
            str += "{{{}: {}}} ".format(n, m)
        return str


    def __del__(self) -> None:
        self._items.clear()
