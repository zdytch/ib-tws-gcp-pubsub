from asyncio import create_task
from gcloud.aio.pubsub import (
    SubscriberClient,
    PublisherClient,
    SubscriberMessage,
    PubsubMessage,
    subscribe,
)
from aiohttp import ClientSession
from pydantic import ValidationError
from schemas import CallbackData, SubmitData, StatusData
from settings import GCP_PROJECT, GCP_STATUS_TOPIC, GCP_SUBMIT_TOPIC_SUB
from typing import Callable, Awaitable
from loguru import logger


class GCPConnector:
    def __init__(self):
        self._status_topic = f'projects/{GCP_PROJECT}/topics/{GCP_STATUS_TOPIC}'
        self._submit_topic_sub = (
            f'projects/{GCP_PROJECT}/subscriptions/{GCP_SUBMIT_TOPIC_SUB}'
        )

    def run(self) -> None:
        create_task(self._listen())

    def set_data_callback(
        self, data_callback: Callable[[CallbackData], Awaitable]
    ) -> None:
        self.data_callback = data_callback

    async def publish_status(self, data: StatusData) -> None:
        async with ClientSession() as session:
            publisher = PublisherClient(session=session)
            messages = [PubsubMessage(data.json())]

            await publisher.publish(self._status_topic, messages)

    async def _listen(self) -> None:
        logger.debug(f'Listening for messages on {self._submit_topic_sub}...')

        subscriber = SubscriberClient()

        await subscribe(self._submit_topic_sub, self._subscriber_callback, subscriber)

    async def _subscriber_callback(self, message: SubscriberMessage) -> None:
        if message.data:
            try:
                data = SubmitData.parse_raw(message.data)

                if hasattr(self, 'data_callback'):
                    await self.data_callback(data)

                else:
                    logger.debug('Cannot send SubmitData, data callback not set')

            except ValidationError as error:
                logger.debug(error)
