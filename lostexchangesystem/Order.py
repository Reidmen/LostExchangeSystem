"""
Author: Reidmen <r.rethmawn@gmail.com>
Order class encapsulates encapsulates all
create, edit and cancel orders.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from Constants import OrderStatus, OrderType, TimeEnforcementType


class OrderBase(ABC):
    @property
    @abstractmethod
    def order_id(self):
        pass

    @property
    @abstractmethod
    def is_bid(self):
        pass

    @property
    @abstractmethod
    def previous_item(self):
        pass

    @property
    @abstractmethod
    def next_item(self):
        pass

    @property
    @abstractmethod
    def root(self):
        pass


class OrderNode:
    def __init__(
        self,
        order_id: int = 0,
        previous_item=None,
        next_item=None,
        count: int = 0,
    ) -> None:
        self.order_id = order_id
        self.previous_item = previous_item
        self.next_item = next_item
        self.count = count

    def __len__(self) -> int:
        return self.count

    def __repr__(self) -> str:
        return f"OrderNode({self.count})"


class Order:
    """Double-Linked list order item."""

    def __init__(
        self,
        order_id: int = 0,
        is_bid: bool = False,
        size: float = 0.0,
        price: float = 0.0,
        root: OrderNode = OrderNode(),
        next_item: OrderNode = OrderNode(),
        previous_item: OrderNode = OrderNode(),
    ) -> None:
        """Initializes order as open, and defines basic attributes
        such as id, is_buy, status and time_enforcement."""
        self.__order_id = order_id
        self.__is_bid = False
        self.__size = size
        self.__price = price
        self.__status = OrderStatus.OPEN
        self.__time_enforcement = TimeEnforcementType.ON_THE_OPEN
        self.__started_time = datetime.now()
        self.__closed_time = None

        self.root = root
        self.next_item = next_item
        self.previous_item = previous_item

        self.order_node = OrderNode(
            order_id=order_id, previous_item=previous_item, next_item=next_item
        )

    @property
    def order_id(self):
        return self.__order_id

    @property
    def is_bid(self):
        return self.__is_bid

    @property
    def size(self):
        return self.__size

    def append(self, order: OrderNode) -> None:
        """Append an order node object"""
        if self.next_item is None:
            self.next_item = order
            self.next_item.previous_item = self.order_node
            # self.next_item.root = self.root

            self.root.count += 1
            self.root.previous_item = order


class SellOrderWithLimit(OrderBase):
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
