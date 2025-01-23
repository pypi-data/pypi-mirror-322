import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from eskmo.utils.logger import Logger as Logger

class Extension(ABC, metaclass=abc.ABCMeta):
    defaultApi: Incomplete
    apis: Incomplete
    def __init__(self, defaultApi) -> None: ...
    @abstractmethod
    def addAPI(self): ...
    @abstractmethod
    def onNewSymbols(self, apitype, data): ...
    @abstractmethod
    def getPIDSubscribeInfo(self, pid, tag): ...
