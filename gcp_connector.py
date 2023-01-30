from asyncio import create_task
from gcloud.aio.pubsub import SubscriberClient, SubscriberMessage, subscribe
from json import loads, JSONDecodeError
from pydantic import ValidationError
from schemas import CallbackData, SubmitData
from settings import GCP_PROJECT_ID, GCP_SUBSCRIPTION_ID
from typing import Callable
from loguru import logger


class GCPConnector:
    def run(self) -> None:
        create_task(self._listen())

    def set_data_callback(self, data_callback: Callable[[CallbackData], None]) -> None:
        self.data_callback = data_callback

    async def _listen(self) -> None:
        subscription_path = (
            f'projects/{GCP_PROJECT_ID}/subscriptions/{GCP_SUBSCRIPTION_ID}'
        )
        subscriber = SubscriberClient()

        logger.debug(f'Listening for messages on {subscription_path}...')

        await subscribe(subscription_path, self._subscriber_callback, subscriber)

    async def _subscriber_callback(self, message: SubscriberMessage) -> None:
        if message.data:
            try:
                json = loads(message.data)
                data = SubmitData(**json)

                if hasattr(self, 'data_callback'):
                    self.data_callback(data)

            except (JSONDecodeError, ValidationError) as error:
                logger.debug(error)
