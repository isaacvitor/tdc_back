from enum import Enum


# ENUM to CallType #
class CallType(str, Enum):
    INBOUND = 'INBOUND'
    OUTBOUND = 'OUTBOUND'
