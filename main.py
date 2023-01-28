from asyncio import Queue, run, create_task, gather
from schemas import CallbackData, SubmitData, StatusData
from gcp_connector import listen
from loguru import logger

_main_queue: Queue = Queue()

logger.add(
    'logs/{time}.log',
    format='{time} {level} {message}',
    level='DEBUG',
    rotation='100 MB',
    retention='14 days',
    compression='zip',
)


async def main():
    t1 = create_task(_dequeue())
    t2 = create_task(listen(_connector_callback))

    await gather(t1, t2)


async def _dequeue() -> None:
    while True:
        data = await _main_queue.get()
        data_type = type(data)

        if data_type == SubmitData:
            logger.debug(data)  # TODO: Submit with IB connector

        elif data_type == StatusData:
            logger.debug(data)  # TODO: Publish with GCP connector

        _main_queue.task_done()


def _connector_callback(data: CallbackData) -> None:
    _main_queue.put_nowait(data)


if __name__ == '__main__':
    run(main())
