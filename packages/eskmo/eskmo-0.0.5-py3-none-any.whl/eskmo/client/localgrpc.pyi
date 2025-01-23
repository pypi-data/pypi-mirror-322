import abc
from eskmo.base.client import Client as Client

class LocalgRPCClient(Client, metaclass=abc.ABCMeta): ...
