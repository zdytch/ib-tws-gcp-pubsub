from gcloud.aio.pubsub import SubscriberClient, SubscriberMessage, subscribe
from json import loads, JSONDecodeError
from pydantic import ValidationError
from schemas import CallbackData, SubmitData
from settings import GCP_PROJECT_ID, GCP_SUBSCRIPTION_ID
from typing import Callable
from loguru import logger

_data_callback: Callable[[CallbackData], None]


async def listen(data_callback: Callable[[CallbackData], None]) -> None:
    global _data_callback
    _data_callback = data_callback

    subscription_path = f'projects/{GCP_PROJECT_ID}/subscriptions/{GCP_SUBSCRIPTION_ID}'
    subscriber = SubscriberClient()

    logger.debug(f'Listening for messages on {subscription_path}...')

    await subscribe(subscription_path, _subscriber_callback, subscriber)


async def _subscriber_callback(message: SubscriberMessage) -> None:
    if message.data:
        try:
            json = loads(message.data)
            data = SubmitData(**json)

            if _data_callback:
                _data_callback(data)

        except (JSONDecodeError, ValidationError) as error:
            logger.debug(error)
