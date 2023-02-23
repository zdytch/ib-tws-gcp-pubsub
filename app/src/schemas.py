from pydantic import BaseModel
from enum import Enum
from decimal import Decimal
from uuid import UUID


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


class OrderStatus(Enum):
    SUBMITTED = 'SUBMITTED'
    PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    FILLED = 'FILLED'
    CANCELLED = 'CANCELLED'


class CallbackData(BaseModel):
    id: UUID


class SubmitData(CallbackData):
    symbol: str
    exchange: Exchange
    side: Side
    type: OrderType
    size: int
    price: Decimal


class StatusData(CallbackData):
    status: OrderStatus
    fill_size: int
    fill_price: Decimal
