from eskmo.base.mvtype import *
from _typeshed import Incomplete
from eskmo.base.client import Client as Client
from eskmo.connection.best5 import Best5Connection as Best5Connection
from eskmo.connection.event import EventConnection as EventConnection
from eskmo.connection.kline import KLineConnection as KLineConnection
from eskmo.connection.quote import QuoteConnection as QuoteConnection
from eskmo.connection.reply import ReplyConnection as ReplyConnection
from eskmo.connection.strategyreply import StrategyReplyConnection as StrategyReplyConnection
from eskmo.internal.user import User as User

class ConsoleClient(Client):
    def __init__(self, config) -> None: ...
    connections: Incomplete
    def initConnections(self) -> None: ...
    def register(self, tag: str, user: User) -> None: ...
