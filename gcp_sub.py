import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_key.json'
SUBSCRIPTION_PATH = 'projects/tsa-test-314819/subscriptions/test_sub'


async def subscribe_signals() -> None:
    subscriber = pubsub_v1.SubscriberClient()
    streaming_pull_future = subscriber.subscribe(SUBSCRIPTION_PATH, callback=callback)

    print(f'Listening for messages on {SUBSCRIPTION_PATH}..\n')

    with subscriber:
        try:
            streaming_pull_future.result()

        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f'Received {message}.')
    message.ack()
