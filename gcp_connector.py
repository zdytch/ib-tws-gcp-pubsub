from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from json import loads, JSONDecodeError
from schemas import CallbackData, SubmitData
from settings import GCP_PROJECT_ID, GCP_SUBSCRIPTION_ID
from typing import Callable
from loguru import logger


class GCPConnector:
    def __init__(self):
        self._subscriber = pubsub_v1.SubscriberClient()

    def set_data_callback(self, data_callback: Callable[[CallbackData], None]) -> None:
        self.data_callback = data_callback

    def subscribe(self) -> None:
        subscription_path = self._subscriber.subscription_path(
            GCP_PROJECT_ID, GCP_SUBSCRIPTION_ID
        )
        streaming_pull_future = self._subscriber.subscribe(
            subscription_path, callback=self._subscriber_callback
        )

        logger.debug(f'Listening for messages on {subscription_path}...')

        with self._subscriber:
            try:
                streaming_pull_future.result()

            except (TimeoutError, KeyboardInterrupt):
                streaming_pull_future.cancel()
                streaming_pull_future.result()

    def _subscriber_callback(
        self, message: pubsub_v1.subscriber.message.Message
    ) -> None:
        message.ack()

        if message.data:
            try:
                json = loads(message.data)
                data = SubmitData(**json)

                if hasattr(self, 'data_callback'):
                    self.data_callback(data)

            except JSONDecodeError as error:
                logger.debug(error)
