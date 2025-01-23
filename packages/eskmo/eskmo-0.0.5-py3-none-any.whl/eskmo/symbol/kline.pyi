from eskmo.base.mvtype import *
from _typeshed import Incomplete
from eskmo.utils.logger import Logger as Logger

class KLine:
    klineIndexMap: Incomplete
    numberKeys: Incomplete
    def getDatetime(self, klinestr): ...
    klineInfo: Incomplete
    infoDict: Incomplete
    def __init__(self, klineInfo) -> None: ...
    def dict(self): ...
