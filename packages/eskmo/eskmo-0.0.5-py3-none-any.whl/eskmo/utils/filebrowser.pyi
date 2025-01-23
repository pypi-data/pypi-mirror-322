from _typeshed import Incomplete

class FileBrowser:
    path: Incomplete
    lock: Incomplete
    isClosed: bool
    @staticmethod
    def run_dialog(is_file: bool = True) -> None: ...
    @staticmethod
    def open(is_file: bool = True) -> None: ...
