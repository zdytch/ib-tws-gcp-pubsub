from gcloud.aio.pubsub import SubscriberClient, subscribe
from typing import Callable
import os

PUBSUB_PROJECT = os.environ['PUBSUB_PROJECT']
PUBSUB_TOPIC = os.environ['PUBSUB_TOPIC']


async def subscribe_signals(handler: Callable) -> None:
    subscriber = SubscriberClient()

    await subscribe(
        f'projects/{PUBSUB_PROJECT}/subscriptions/{PUBSUB_TOPIC}',
        handler,
        subscriber,
        num_producers=1,
        max_messages_per_producer=100,
        ack_window=0.3,
        num_tasks_per_consumer=1,
        enable_nack=True,
        nack_window=0.3,
    )
