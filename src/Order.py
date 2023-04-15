"""
Order class encapsulares all buy and sell orders.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from Constants import OrderStatus, TimeEnforcementType


class Order(ABC):
    def __init__(self, id_: str):
        self.__order_id = id_
        self.__is_buy_order = False
        self.__status = OrderStatus.OPEN
        self.__time_enforcement = TimeEnforcementType.ON_THE_OPEN
        self.__started_time = datetime.now()

        self.__parts = {}

    def set_new_status(self, status: dict):
        self.status = status

    # TODO add methods to store in a database

    def add_order_parts(self, parts: list):
        for part in parts:
            self.__parts[part.get_id()] = part


class LimitOrder(Order):
    def __init__(self):
        self.__price_limit = 0.0
