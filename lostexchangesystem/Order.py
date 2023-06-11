"""
Author: Reidmen <r.rethmawn@gmail.com>
Order class encapsulates encapsulates all
create, edit and cancel orders.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from Constants import OrderStatus, OrderType, TimeEnforcementType


class Order(ABC):
    def __init__(self, _id: str):
        """Initializes order as open, and defines basic attributes
        such as id, is_buy, status and time_enforcement."""
        self.__order_id = _id
        self.__is_buy_order = False
        self.__status = OrderStatus.OPEN
        self.__time_enforcement = TimeEnforcementType.ON_THE_OPEN
        self.__started_time = datetime.now()
        self.__closed_time = None

    @property
    @abstractmethod
    def order_id(self):
        return self.__order_id

    @property
    @abstractmethod
    def is_buy_order(self):
        return self.__is_buy_order

    @property
    @abstractmethod
    def status(self):
        return self.__status

    @abstractmethod
    def set_new_status(self, status: OrderStatus):
        """Encapsulates editing the order status, which includes
        cancelling"""
        self.__status = status

    @abstractmethod
    def set_close_time(self, time: datetime):
        """Set closed time for order in case cancelled
        or fully/partially filled."""
        self.__closed_time = time


class SellOrderWithLimit(Order):
    def __init__(self, _id, quantity, limit_price, enforcement_type):
        self.__order_id = _id
        self.__is_buy_order = False
        self.__status = OrderStatus.OPEN
        self.__order_type = OrderType.SELL
        self.__time_enforcement = TimeEnforcementType.ON_THE_OPEN
        self.__started_time = datetime.now()
        self.__closed_time = None
        self.__limit_price = limit_price

    @property
    def order_id(self):
        return self.__order_id

    @property
    def is_buy_order(self):
        return self.__is_buy_order

    @property
    def status(self):
        return self.__status

    def save_to_database(self):
        """Save order to database."""
        return NotImplementedError("Instantiate databased (NOSQL / H5)")

    def set_new_status(self, status: OrderStatus):
        """Encapsulates editing the order status, which includes
        cancelling"""
        self.__status = status

    def set_close_time(self, time: datetime):
        """Set closed time for order in case cancelled
        or fully/partially filled."""
        self.__closed_time = time


class BuyOrderWithLimit(Order):
    def __init__(self, _id, quantity, limit_price, enforcement_type):
        self.__order_id = _id
        self.__is_buy_order = False
        self.__status = OrderStatus.OPEN
        self.__order_type = OrderType.BUY
        self.__time_enforcement = TimeEnforcementType.ON_THE_OPEN
        self.__started_time = datetime.now()
        self.__closed_time = None
        self.__limit_price = limit_price

    @property
    def order_id(self):
        return self.__order_id

    @property
    def is_buy_order(self):
        return self.__is_buy_order

    @property
    def status(self):
        return self.__status

    def save_to_database(self):
        """Save order to database."""
        return NotImplementedError("Instantiate databased (NOSQL / H5)")

    def set_new_status(self, status: OrderStatus):
        """Encapsulates editing the order status, which includes
        cancelling"""
        self.__status = status

    def set_close_time(self, time: datetime):
        """Set closed time for order in case cancelled
        or fully/partially filled."""
        self.__closed_time = time
