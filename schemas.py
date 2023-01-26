from pydantic import BaseModel
from enum import Enum
from decimal import Decimal


class Exchange(Enum):
    NYSE = 'NYSE'
    NASDAQ = 'NASDAQ'


class Side(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderType(Enum):
    LIMIT = 'LMT'
    STOP = 'STP'
    MARKET = 'MKT'


class CallbackData(BaseModel):
    pass


class SubmitData(CallbackData):
    symbol: str
    exchange: Exchange
    side: Side
    type: OrderType
    size: int
    price: Decimal = Decimal('0.0')


class StatusData(CallbackData):
    ...
