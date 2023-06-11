"""The StockExchange class encapsulates the interaction
between the client with Orders (sending, canceling, editing orders)
to the API of the Exchange (such as. Interactive Brokers, Binance, etc)."""
from .Order import Order

class StockExchange:
    # we expect a single instance 
    __initialized = False

    def __init__(self):
        if not StockExchange.__initialized:
            StockExchange.__initialized = True


    def send_order_to_market(self, order: Order):
        status = self.get_instance().submit_order(order)
        return status
