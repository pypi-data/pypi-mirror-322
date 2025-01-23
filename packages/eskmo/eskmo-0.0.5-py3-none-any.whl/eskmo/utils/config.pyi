from _typeshed import Incomplete

DEV_MODE: str
PROD_MODE: str
DEV_METRIC_MODE: str
TRUE_TEXT: str
FALSE_TEXT: str
ENV_ACCOUNT: str
ENV_PASSWORD: str
ENV_LOG_LEVEL: str
ENV_MODE: str
ENV_SANDBOX: str
ENV_RECORDING: str
ENV_APP_KEY_VERIFY: str
ENV_APP_KEY: str
ENV_LOG_FILE: str
ENV_PROJECT_NAME: str
CONFIG_DEFAULT: Incomplete
CONFIG_ACCOUNT: Incomplete
CONFIG_PASSWORD: Incomplete
CONFIG_LOG_LEVEL: Incomplete
CONFIG_SANDBOX: Incomplete
CONFIG_RECORDING: Incomplete
CONFIG_APP_KEY_VERIFY: Incomplete
CONFIG_MODE: Incomplete
CONFIG_APP_KEY: Incomplete
CONFIG_LOG_FILE: Incomplete
CONFIG_PROJECT_NAME: Incomplete

class Config:
    @staticmethod
    def isSandboxMode(): ...
    @staticmethod
    def isRecording(): ...
    @staticmethod
    def isAppKeyVerify(): ...
    @staticmethod
    def isAutoLogin(): ...
    @staticmethod
    def mode(): ...
    @staticmethod
    def account(): ...
    @staticmethod
    def password(): ...
