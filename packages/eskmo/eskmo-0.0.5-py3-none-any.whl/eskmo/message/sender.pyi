from _typeshed import Incomplete
from eskmo.base.mvtype import THREAD_ZMQ_PREFIX as THREAD_ZMQ_PREFIX
from eskmo.client.localzmq import DEFAULT_ENCODING as DEFAULT_ENCODING
from eskmo.message.const import NUM_ZMQ_SEND_CAPACITY as NUM_ZMQ_SEND_CAPACITY

API_FUNCTION: str
SKO_SEND_STOCK_ORDER: str
API_TOPIC: str
API_COUNT: str

class ZMQTopicSender:
    sendCnt: Incomplete
    capacity: Incomplete
    context: Incomplete
    socket: Incomplete
    topic: Incomplete
    queue: Incomplete
    bTopic: Incomplete
    counter: Incomplete
    sendQueue: Incomplete
    logger: Incomplete
    sendingDoneCount: int
    def __init__(self, topic, context, socket, logger) -> None: ...
    def listenForSend(self) -> None: ...
    def sendCall(self, data, topic) -> None: ...
    def send(self, data, topic: Incomplete | None = None) -> None: ...
