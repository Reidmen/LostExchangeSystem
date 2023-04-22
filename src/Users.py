"""User class introduces logic required for an order to exist given
the user available money, preferences, etc., and manages client requests from and to the Brokerage."""

from datetime import datetime
from .Order import SellOrderWithLimit, BuyOrderWithLimit
from .Constants import OrderStatus, AccountStatus, ReturnStatus, TimeEnforcementType
from .StockExchange import StockExchange


class User(Account):
    """Introduces basic user logic based on buy/sell orders"""
    def __init__(self):
        self.__available_funds = 0.0
        self.__membership_date = datetime.date.today()
        self.__stock_positions = {}
        self.__active_orders = {}
        self.__cancelled_orders = {}

    def place_sell_order_with_limit(
        self,
        stock_id: str,
        quantity: int,
        limit_price: float,
        enforcement_type: TimeEnforcementType,
    ):
        # check if there are already positions to sell
        if options_id not in self.__stock_positions:
            return ReturnStatus.NO_STOCKS_POSITION

        stock_position = self.__stock_positions[stock_id]
        # check if user has enoguh quantity to sell
        if stock_position.get_quantity() < quantity:
            return ReturnStatus.INSUFFICIENT_QUANTITY

        # create an order
        order = SellOrderWithLimit(stock_id, quantity, limit_price, enforcement_type)

        order.is_buy_order = False
        order.save_to_database()
        try:
            success = StockExchange.send_order_to_market(order)
            order.set_new_status(OrderStatus.NOT_CANCELLED)
        except StockExchange.SEND_ORDER_ERROR:
            print(
                "Order not successfully submitted into the Exchange "
                "with message: {}".format(success)
            )
            order.set_new_status(OrderStatus.CANCELLED)
        else:
            self.__active_orders[order.order_id] = Order

        return success

    def place_buy_order_with_limit(
            self,
            stock_id: str,
            quantity: int,
            limit_price: float,
            enforcement_type: TimeEnforcementType,):
        # check if enough money to buy stock
        if self.__available_funds < quantity * limit_price:
            return ReturnStatus.INSUFFICIENT_FUNDS

        order = BuyOrderWithLimit(stock_id, quantity, limit_price, enforcement_type)

        order.is_buy_order = False
        order.save_to_database()
        try:
            success = StockExchange.send_order_to_market(order)
            order.set_new_status(OrderStatus.NOT_CANCELLED)
        except StockExchange.SEND_ORDER_ERROR:
            print(
                "Order not successfully submitted into the Exchange "
                "with message: {}".format(success)
            )
            order.set_new_status(OrderStatus.CANCELLED)
        else:
            self.__active_orders[order.order_id] = order

        return success


    def callback_from_stock_exchange(self,
            order_id,
            status):
        """Introduces callback method to get response from
        the stock exchange or brokerage"""
        order = self.__act[order_id]
        order.set_status(status)
        order_save_to_database()

        if status == OrderStatus.FILLED or status == OrderStatus.CANCELLED:
            self.__active_orders.pop(order_id)
