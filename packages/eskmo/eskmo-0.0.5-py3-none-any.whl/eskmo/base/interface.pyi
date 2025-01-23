from _typeshed import Incomplete
from abc import ABC
from eskmo.internal.api import api as api
from eskmo.internal.user import User as User

class UserReferable(ABC):
    user: Incomplete
    accountIds: Incomplete
    def __init__(self, user: User) -> None: ...

class APIReferable(ABC):
    api: Incomplete
    def __init__(self, api: api) -> None: ...
