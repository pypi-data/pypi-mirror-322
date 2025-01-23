import zmq
from _typeshed import Incomplete
from eskmo.base.client import Client as Client
from eskmo.base.mvtype import API_ARGS as API_ARGS, API_KWARGS as API_KWARGS, BEST5 as BEST5, COMMAND as COMMAND, EVENT as EVENT, EVENT_DATA as EVENT_DATA, KLINE as KLINE, PID as PID, PING as PING, PONG as PONG, QUOTE as QUOTE, REPLY as REPLY, STRATEGY_REPLY as STRATEGY_REPLY, USER as USER
from eskmo.internal.api import api as api
from eskmo.internal.user import User as User
from eskmo.utils.misc import threadStart as threadStart
from eskmo.utils.thread import ThreadHandler as ThreadHandler

DEFAULT_ZMQ_PORTS: Incomplete
DEFAULT_ENCODING: str

class ZMQReceiver:
    api: Incomplete
    context: Incomplete
    socket: Incomplete
    topic: Incomplete
    def __init__(self, api: api, topic: str, context: zmq.Context, socket: zmq.Socket) -> None: ...
    def start(self) -> None: ...

class ZMQListener:
    context: Incomplete
    socket: Incomplete
    topic: Incomplete
    bTopic: Incomplete
    queue: Incomplete
    def __init__(self, topic, context, socket, isSequential: bool = False) -> None: ...
    @property
    def command(self): ...
    def startListen(self, workerNum) -> None: ...
    def start(self) -> None: ...
    def add(self, pid: str, event: str, data: dict): ...

class LocalZMQClient(Client):
    api: Incomplete
    def __init__(self, api: api, config) -> None: ...
    receivers: Incomplete
    def initReceivers(self) -> None: ...
    ports: Incomplete
    def initConfig(self) -> None: ...
    context: Incomplete
    pub_socket: Incomplete
    rep_socket: Incomplete
    def initSocket(self) -> None: ...
    connections: Incomplete
    def initConnections(self) -> None: ...
    def register(self, tag: str, user: User) -> None: ...
