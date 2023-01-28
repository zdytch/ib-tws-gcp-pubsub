from gcloud.aio.pubsub import SubscriberClient, SubscriberMessage, subscribe
from json import loads, JSONDecodeError
from schemas import CallbackData, SubmitData
from settings import GCP_PROJECT_ID, GCP_SUBSCRIPTION_ID
from typing import Callable
from loguru import logger

_data_callback: Callable[[CallbackData], None]


async def listen(data_callback: Callable[[CallbackData], None]) -> None:
    global _data_callback
    _data_callback = data_callback

    subscriber = SubscriberClient()
    await subscribe(
        f'projects/{GCP_PROJECT_ID}/subscriptions/{GCP_SUBSCRIPTION_ID}',
        _subscriber_callback,
        subscriber,
        num_producers=1,
        max_messages_per_producer=100,
        ack_window=0.3,
        num_tasks_per_consumer=1,
        enable_nack=True,
        nack_window=0.3,
    )


async def _subscriber_callback(message: SubscriberMessage) -> None:
    if message.data:
        try:
            json = loads(message.data)
            data = SubmitData(**json)

            if _data_callback:
                _data_callback(data)

        except JSONDecodeError as error:
            logger.debug(error)
