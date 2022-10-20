import traceback
from time import sleep

import paho.mqtt.client as mqtt

import structlog
log = structlog.get_logger()

GENERATOR_TOPIC = 'generator'
AGGREGATOR_TOPIC = 'aggregator'
REPORTER_TOPIC = 'reporter'
BROKER_HOSTNAME = 'mosquitto'

PAYLOAD_NUMBER_KEY = 'number'
PAYLOAD_TIMESTAMP_KEY = 'timestamp'

PAYLOAD_ONE_MINUTE_KEY = "one_minute"
PAYLOAD_FIVE_MINUTE_KEY = "five_minute"
PAYLOAD_THIRTY_MINUTE_KEY = "thirty_minute"