from eskmo.base.interface import UserReferable as UserReferable

class Quotes(UserReferable):
    def __init__(self, user) -> None: ...

class Quote(UserReferable):
    def __init__(self, user) -> None: ...
