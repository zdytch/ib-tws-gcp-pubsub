import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_key.json'

GCP_PROJECT = os.getenv('GCP_PROJECT')
GCP_STATUS_TOPIC = os.getenv('GCP_STATUS_TOPIC')
GCP_SUBMIT_TOPIC_SUB = os.getenv('GCP_SUBMIT_TOPIC_SUB')
