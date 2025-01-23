from eskmo.const.skcom import *
from _typeshed import Incomplete
from dataclasses import dataclass as dataclass, field as field
from eskmo.utils.thread import ThreadHandler as ThreadHandler

EXTENSION_NAME: str
RECORDING_PATH: str
RECORDING_TASK_PATH: Incomplete
RECORDING_FUNCTION: str
RECORDING_TIMESTAMP: str
RECORDING_ARGS: str
RECORDING_KWARGS: str
RECORDING_HANDLER: str
RECORDING_MODE_FILE: str
RECORDING_MODE_DB: str
RECORDING_MODES: Incomplete

class SKRecorder:
    api: Incomplete
    handlers: Incomplete
    events: Incomplete
    files: Incomplete
    funcMaps: Incomplete
    mode: Incomplete
    thread: Incomplete
    def __init__(self, api, threads: int = 1) -> None: ...
    def getFilePathByFunc(self, filename): ...
    def register(self, handlerName, events) -> None: ...
    def isRecordRequired(self, funcName): ...
    def writeToFile(self, data, filepath) -> None: ...
    def writeData(self, funcName, data) -> None: ...
    def addTask(self, funcName, *args, **kwargs) -> None: ...
    def __del__(self) -> None: ...
