from random import randrange
from time import sleep
from sys import stdout
import traceback
import json
from datetime import datetime

import mqtt_common
import paho.mqtt.publish as publish

import structlog

log = structlog.get_logger()


def send_generated_number(number):
    log.msg("Generated number", number=number)
    payload = json.dumps(
        {
            mqtt_common.PAYLOAD_NUMBER_KEY: number,
            mqtt_common.PAYLOAD_TIMESTAMP_KEY: datetime.utcnow().isoformat(),
        }
    )
    try:
        response = publish.single(
            mqtt_common.GENERATOR_TOPIC, payload, hostname=mqtt_common.BROKER_HOSTNAME
        )
        log.msg("Publish Response", response=response)
    except Exception as e:
        log.error("Publish Traceback", traceback=traceback.format_exc())


if __name__ == "__main__":
    stop_loop = False
    while not stop_loop:
        generated_number = randrange(1, 100, 1)

        send_generated_number(generated_number)

        interval = randrange(1, 5, 1)
        log.msg("Sleeping", interval=interval)
        sleep(interval)
