from asyncio import Queue, run, create_task
from schemas import CallbackData, SubmitData, StatusData

_main_queue: Queue = Queue()


async def main():
    create_task(_dequeue())


async def _dequeue() -> None:
    while True:
        data = await _main_queue.get()
        data_type = type(data)

        if data_type == SubmitData:
            ...  # Submit with IB connector

        elif data_type == StatusData:
            ...  # Publish with GCP connector

        _main_queue.task_done()


def _connector_callback(data: CallbackData) -> None:
    _main_queue.put_nowait(data)


if __name__ == '__main__':
    run(main())
