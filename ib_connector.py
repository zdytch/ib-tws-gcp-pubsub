from asyncio import create_task
from ib_insync import IB, Order, Stock, Trade, Contract
from schemas import CallbackData, SubmitData, StatusData, OrderStatus, OrderType
from decimal import Decimal
from uuid import UUID
from typing import Callable
from loguru import logger


class IBConnector:
    def __init__(self):
        self._ib = IB()
        self._ib.errorEvent += self._error_callback
        self._ib.orderStatusEvent += self._order_status_callback

    def run(self) -> None:
        create_task(self._connect())

    def is_connected(self) -> bool:
        return self._ib.isConnected()

    def set_data_callback(self, data_callback: Callable[[CallbackData], None]) -> None:
        self.data_callback = data_callback

    async def submit_order(self, data: SubmitData) -> None:
        await self._connect()

        if self.is_connected():
            contract = Stock(data.symbol, f'SMART:{data.exchange.value}', 'USD')
            order = self._create_order(data)

            self._ib.placeOrder(contract, order)

        else:
            logger.debug('Cannot submit order, IB disconnected')

    async def _connect(self):
        if not self.is_connected():
            try:
                await self._ib.connectAsync('localhost', 4002, 1)

            except Exception as error:
                logger.debug(error)

    def _create_order(self, data: SubmitData) -> Order:
        order = Order(
            orderId=self._ib.client.getReqId(),
            orderRef=str(data.id),
            action=data.side.value,
            orderType=data.type.value,
            totalQuantity=float(data.size),
            tif='DAY',
            transmit=True,
        )

        if data.type == OrderType.LIMIT:
            order.lmtPrice = float(data.price)

        elif data.type == OrderType.STOP:
            order.auxPrice = float(data.price)

        return order

    async def _error_callback(
        self, req_id: int, code: int, message: str, contract: Contract | None
    ) -> None:
        logger.debug(f'{req_id} {code} {message} {contract if contract else ""}')

    def _order_status_callback(self, trade: Trade) -> None:
        logger.debug(f'IB trade changed: {trade}')

        if hasattr(self, 'data_callback'):
            ib_status = trade.orderStatus.status
            fill_size = int(trade.orderStatus.filled)
            fill_price = Decimal(str(trade.orderStatus.avgFillPrice))
            status = None

            if ib_status == 'Filled':
                status = OrderStatus.FILLED

            elif ib_status == 'Submitted' and fill_size:
                status = OrderStatus.PARTIALLY_FILLED

            elif ib_status in ('PendingSubmit', 'PreSubmitted', 'Submitted'):
                status = OrderStatus.SUBMITTED

            elif ib_status == 'Cancelled' and not fill_size:
                status = OrderStatus.CANCELLED

            if status:
                data = StatusData(
                    id=UUID(trade.order.orderRef),
                    status=status,
                    fill_size=fill_size,
                    fill_price=fill_price,
                )

                self.data_callback(data)

        else:
            logger.debug('Cannot send OrderStatus, data callback not set')
