# Interactive Brokers TWS with Google Cloud PubSub
This simple app shows how use GCP PubSub as an input/output for IB TWS. 
It allows to submit stock orders to IB and receive status updates from IB TWS

The app listens to a GCP topic subscription and translates queue messages to order data for IB TWS. At the same time, it listens to events from IB TWS and translates them to queue messages for GCP topic.

## Setup

### Prepare environment
- Clone the repository: `git clone https://github.com/zdytch/ib-tws-gcp-pubsub-asyncio.git`
- Switch to the project directory: `cd /path/to/project/directory`
- Create a copy of environment file from the sample: `cp .env.sample .env`
- Open .env file with any text editor, e.g.: `nano .env`
- You will see variables with sample values. Replace the values with your own ones

### Prepare GCP PubSub key file
- Get a JSON key file from [GCP service accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts)
- Put the key file in the path: `/app/src/gcp_key.json`

### Environment variables explained
- GCP_PROJECT: name of GCP PubSub project
- GCP_STATUS_TOPIC: name of the topic where to publish order status updates
- GCP_SUBMIT_TOPIC_SUB: name of the topic subscription from where to pull data to submit orders

- TIME_ZONE: timezone name. Affects time in IB application. All TZ names are available [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

- COMPOSE_PROJECT_NAME: used by docker engine to label images, doesn't affect the application

## Usage

Publish a JSON-formatted message to the submit GCP topic:
```
{"id": "b5de42e4-16e6-4e3c-839a-eb55d62f0205", "symbol": "AAPL", "exchange": "NASDAQ", "side": "BUY", "type": "MKT", "size": 1, "price": 0.0}
```
This submits a market buy order of size 1 for NASDAQ:AAPL

The `id` field used to syncronize with external order logic

After the order submitted, status update messages will appear in status GCP topic

### Supported data types
- Exchanges: `NYSE`, `NASDAQ`
- Sides: `BUY`, `SELL`
- Order types: `LMT`, `STP`, `MKT`
- Order statuses: `SUBMITTED`, `PARTIALLY_FILLED`, `FILLED`, `CANCELLED`
