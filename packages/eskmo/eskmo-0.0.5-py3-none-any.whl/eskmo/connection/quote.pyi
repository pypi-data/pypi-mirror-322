from eskmo.base.mvtype import *
from eskmo.const.event import *
from _typeshed import Incomplete
from eskmo.base.mvqueue import mvQueue as mvQueue
from eskmo.connection.base import mvConnection as mvConnection
from eskmo.utils.logger import Logger as Logger
from multiprocessing import Queue as Queue

class QuoteConnection(mvConnection):
    queues: Incomplete
    def __init__(self) -> None: ...
    def add(self, id, event=..., data={}) -> None: ...
    def addProcessQueues(self, queues: list['mvQueue']): ...
    def listen(self, conns, queues) -> None: ...
