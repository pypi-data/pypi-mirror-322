from eskmo.base.interface import UserReferable as UserReferable

class Streams(UserReferable):
    def __init__(self, user) -> None: ...

class Stream(UserReferable):
    def __init__(self, user) -> None: ...
