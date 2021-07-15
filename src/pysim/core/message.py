class Message:
    def __init__(self, *, text: str = None) -> None:
        self._text: str = text
        self._src: str = None
        self._dest: str = None


    def get_text(self) -> str:
        return self._text


    def set_source(self, src) -> None:
        self._src = src


    def get_source(self) -> str:
        return self._src


    def set_dest(self, dest) -> None:
        self._dest = dest


    def get_dest(self) -> str:
        return self._dest


    def is_self_message(self) -> bool:
        return self._src == self._dest
