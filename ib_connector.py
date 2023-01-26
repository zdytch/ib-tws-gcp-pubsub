from ib_insync import IB, Order as IBOrder, Stock, Trade
from schemas import SubmitData
from loguru import logger


class IBConnector:
    def __init__(self):
        self._ib = IB()
        self._ib.orderStatusEvent += self._order_status_callback

    async def submit_order(self, data: SubmitData) -> None:
        await self._connect()

        if self._ib.isConnected():
            contract = Stock(data.symbol, f'SMART:{data.exchange}', 'USD')
            ib_order = IBOrder(
                orderId=self._ib.client.getReqId(),
                action=data.side.value,
                orderType=data.type.value,
                totalQuantity=float(data.size),
                tif='DAY',
                transmit=True,
            )

            self._ib.placeOrder(contract, ib_order)

    async def _connect(self):
        if not self._ib.isConnected():
            try:
                await self._ib.connectAsync('localhost', 4002, 1)

            except Exception as error:
                logger.debug(error)

    def _order_status_callback(self, trade: Trade) -> None:
        logger.debug(f'IB trade changed: {trade}')
