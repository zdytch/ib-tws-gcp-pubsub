from asyncio import Queue, run, create_task
from schemas import CallbackData

_main_queue: Queue = Queue()


async def main():
    create_task(_dequeue())


async def _dequeue() -> None:
    while True:
        ...

        _main_queue.task_done()


def _connector_callback(data: CallbackData) -> None:
    _main_queue.put_nowait(data)


if __name__ == '__main__':
    run(main())
