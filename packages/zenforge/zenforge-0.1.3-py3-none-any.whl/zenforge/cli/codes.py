from enum import Enum


class SetupSuccessCodes(Enum):
    TEST_SUCCESS = -2
    COMPLETE = 10
    ALREADY_CONFIGURED = 11


class CommonErrorCodes(Enum):
    TEST_ERROR = -1
    PROJECT_EXISTS = 20
    UNKNOWN_ERROR = 1000
