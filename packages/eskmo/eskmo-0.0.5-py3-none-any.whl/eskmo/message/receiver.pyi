import abc
from _typeshed import Incomplete
from abc import abstractmethod
from eskmo.base.mvtype import API_COUNT as API_COUNT
from eskmo.client.localzmq import DEFAULT_ENCODING as DEFAULT_ENCODING
from eskmo.message.const import NUM_ZMQ_RECV_CAPACITY as NUM_ZMQ_RECV_CAPACITY, THREAD_ZMQ_PREFIX as THREAD_ZMQ_PREFIX

class ZMQTopicReceiver(metaclass=abc.ABCMeta):
    sendOrderCounter: Incomplete
    logger: Incomplete
    context: Incomplete
    socket: Incomplete
    topic: Incomplete
    queue: Incomplete
    lastCount: Incomplete
    recvLock: Incomplete
    def __init__(self, topic, queue, context, socket, logger) -> None: ...
    def isValidCount(self, cnt): ...
    @abstractmethod
    def isValidCondition(self, data): ...
    def addCountCheck(self, data, cnt) -> None: ...
    @abstractmethod
    def runOnData(self, data): ...
    def start(self) -> None: ...
    def onData(self, data) -> None: ...
