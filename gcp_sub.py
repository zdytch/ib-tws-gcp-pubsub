import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from json import loads, JSONDecodeError
from schemas import CallbackData, SubmitData
from typing import Callable

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_key.json'
SUBSCRIPTION_PATH = 'projects/tsa-test-314819/subscriptions/test_sub'


class GCPConnector:
    def __init__(self):
        self._subscriber = pubsub_v1.SubscriberClient()

    def set_data_callback(self, data_callback: Callable[[CallbackData], None]) -> None:
        self.data_callback = data_callback

    def subscribe(self) -> None:
        streaming_pull_future = self._subscriber.subscribe(
            SUBSCRIPTION_PATH, callback=self._subscriber_callback
        )

        print(f'Listening for messages on {SUBSCRIPTION_PATH}..\n')

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
                print(error)
