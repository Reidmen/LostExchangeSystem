from enum import Enum

# Using PEP435 for enumeration of unique, constant values
class ReturnStatus(Enum):
    SUCCESS = 0
    FAIL = 1
    INSUFFICIENT_FUNDS = 2
    INSUFFICIENT_QUANTITY = 3
    NO_STOCKS_POSITION = 4


class OrderStatus(Enum):
    OPEN = 0
    FILLED = 1
    PARTIALLY_FILLED = 2
    CANCELLED = 3
    NOT_CANCELLED = 4


class OrderType(Enum):
    BUY = 1
    SELL = 2


class AccountStatus(Enum):
    ACTIVE = 0
    CLOSED = 1
    CANCELED = 2
    BACKLISTED = 3
    NONE = 4


class TimeEnforcementType(Enum):
    GOOD_TILL_CANCELLED = 0
    FILL_OR_KILL = 1
    IMMEDIATE_OR_CANCEL = 2
    ON_THE_OPEN = 3
    ON_THE_CLOSED = 4

