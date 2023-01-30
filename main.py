from asyncio import Queue, run
from schemas import CallbackData, SubmitData, StatusData
from ib_connector import IBConnector
from gcp_connector import GCPConnector
from loguru import logger

_main_queue: Queue = Queue()
_ib_connector = IBConnector()
_gcp_connector = GCPConnector()

logger.add(
    'logs/{time}.log',
    format='{time} {level} {message}',
    level='DEBUG',
    rotation='100 MB',
    retention='14 days',
    compression='zip',
)


async def main():
    _ib_connector.set_data_callback(_connector_callback)
    _ib_connector.run()

    _gcp_connector.set_data_callback(_connector_callback)
    _gcp_connector.run()

    await _dequeue()


async def _dequeue() -> None:
    while True:
        data = await _main_queue.get()
        data_type = type(data)

        if data_type == SubmitData:
            await _ib_connector.submit_order(data)

        elif data_type == StatusData:
            await _gcp_connector.publish_status(data)

        _main_queue.task_done()


def _connector_callback(data: CallbackData) -> None:
    _main_queue.put_nowait(data)


if __name__ == '__main__':
    run(main())
