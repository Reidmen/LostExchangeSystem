from dataclasses import dataclass
import datetime

from typing import Union


@dataclass(frozen=False)
class Order:
    symbol: Union[str, None] = "EMPTY"
    position: Union[str, None] = "NULL"
    quantity: Union[float, None] = 0.0
    price: Union[float, None] = 0.0
    date: datetime.datetime = datetime.datetime.now()
    representation: Union[str, None] = "NO_ORDER"

    def __post_init__(self) -> None:
        if self.representation is not None:
            self.representation = f"({self.symbol}, {self.position}, {self.quantity}, {self.price})\n"
