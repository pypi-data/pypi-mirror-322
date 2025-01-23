import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from eskmo.base.mvqueue import mvQueue as mvQueue
from eskmo.base.mvtype import PROCESS_QUEUES as PROCESS_QUEUES
from eskmo.internal.user import User as User

class Client(ABC, metaclass=abc.ABCMeta):
    config: Incomplete
    users: Incomplete
    queues: Incomplete
    def __init__(self, config) -> None: ...
    def createProcessQueues(self, postfix: str) -> list[mvQueue]: ...
    def register(self, tag, user: User) -> list[mvQueue]: ...
    connections: Incomplete
    @abstractmethod
    def initConnections(self): ...
